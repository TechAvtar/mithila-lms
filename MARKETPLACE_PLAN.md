# Mithila LMS: multi-seller marketplace plan

**Status:** Phase 0 built and checked locally, except for putting the local fixes into git. The app holds only the hook checks; no marketplace features exist yet.
**Model:** one site and one shared database. Sellers publish courses and batches, the platform collects the money, takes a commission and pays sellers.

---

## 1. Core decision: a separate Frappe app, no edits to `lms`

Build a new app, `mithila_marketplace`, with `required_apps = ["frappe/lms"]`. All behaviour is added through its `hooks.py`.

- Upstream `frappe/lms` updates can still be pulled with few or no conflicts.
- Frappe combines hooks across apps, so the new app can add to the LMS rules without touching them. Checked in upstream Frappe `develop`:
  - `has_permission`: every registered hook must pass, and hooks can only deny (`frappe/permissions.py`, `has_controller_permissions`).
  - `permission_query_conditions`: conditions from all apps are collected together (`frappe/model/db_query.py`).

**Phase 0 result, on the installed Frappe `17.0.0-dev`** (`docker/mithila_marketplace/mithila_marketplace/probe.py`, 11/11 checks passed):

- Our `has_permission` hook can deny access the LMS would allow, and can't override an LMS denial.
- Query conditions from both apps are combined with AND.
- `frappe.get_all` ignores our conditions, so the endpoint audit in section 6 is needed.
- Our `validate` hook runs after the LMS controller and has the last word, so the review design in section 3 holds.

**Risk found:** `init.sh` installs whatever is latest on the `develop` branches of Frappe, Payments and the fork, so a rebuild can pull in different code. Pin versions before Phase 4 at the latest.

### What already works for sellers

| Existing LMS behaviour | Why it helps | Where |
|---|---|---|
| `Course Creator` role can create courses | It can act as the seller role | `lms_course.json` permissions |
| Only listed instructors can edit a course or batch | Sellers are already separated from each other on authoring | `can_modify_course`, `lms/lms/utils.py` |
| Coupons are limited to the courses a user teaches | Sellers can run their own discounts | `coupon_has_permission`, `permissions.py` |
| Enrolments and submissions are limited to the course's staff | Sellers only see their own students | `permissions.py` |
| `status` field: In Progress / Under Review / Approved | The review flow has a place to live | `lms_course.json` |

**Rule:** a seller gets `Course Creator` only. They must never get `Moderator`, which is unrestricted across the site, or `Batch Evaluator`, which reaches the staff views of every published batch.

---

## 2. Each need mapped to a Frappe feature

"Python" means how much custom logic is needed.

| Need | Frappe feature | Python |
|---|---|---|
| Seller application form | **Web Form** on `Marketplace Seller` | None |
| Approve or reject sellers | **Workflow** on `Marketplace Seller` | None |
| Application and approval emails | **Notification** records, shipped as fixtures | None |
| Grant the seller role on approval | `doc_events` → `Marketplace Seller.on_update` | About 5 lines |
| Link a course or batch to its seller | **Custom Field** `seller`, shipped as a fixture | None |
| Fill in `seller` and stop it being changed | `doc_events` → `LMS Course` / `LMS Batch`: `before_insert`, `validate` | Small |
| Send new courses to review | `doc_events` → `LMS Course.validate` (section 3) | Small |
| Stop sellers setting `featured` | Same `validate` hook | Small |
| Hide other sellers' question banks | `has_permission` → `LMS Question` (section 6) | Small |
| Calculate commission and earnings | `scheduler_events` sweep (section 4) | Medium |
| Release earnings after the hold period | `scheduler_events.daily` | Small |
| Block commission-free "offline" payments | `doc_events` → `LMS Payment.before_insert` (section 4) | Small |
| Limit ledger and payouts to the seller's own rows | `permission_query_conditions` and `has_permission`, or scoped **User Permissions** | Small |
| Payout runs | **Submittable DocType** with `on_submit` and `on_cancel` | Small |
| Monthly seller statements | **Auto Email Report** | None |
| Admin earnings reports | **Script Report**, **Number Card**, **Workspace** | Small |
| Seller dashboard | **www page** in the new app (Jinja, no Vue) | Small |
| Link to the dashboard in the LMS | **LMS Sidebar Item** (types: `Route`, `External`, `Web Page`), as a fixture | None |
| Public seller storefront | `website_route_rules` and a www page | Small |
| Seller name in API responses | `override_whitelisted_methods` wrapper, only if needed | Small |

### New DocTypes

- **Marketplace Settings** (single): default commission %, hold days, minimum payout.
- **Marketplace Seller:** user, display name, status, optional commission override, tax details, payout details (`Password` fieldtype for bank data).
- **Seller Ledger Entry:** `payment` (unique), seller, course or batch, gross, GST, commission rate, commission, net, currency, status (`Pending` / `Available` / `Paid` / `Reversed`), available-on date.
- **Seller Payout** (submittable): seller, period, ledger rows, total, bank reference.

---

## 3. Course review

Today a `Course Creator` can publish their own course: `published` has no field-level restriction, and `validate_status` then marks it Approved.

A `validate` hook can change this with no frontend edit, because controller code runs first and hooks run after it:

```python
def course_validate(doc, method=None):
    if is_marketplace_admin():
        return
    if doc.published and (doc.is_new() or doc.has_value_changed("published")):
        doc.published = 0
        doc.status = "Under Review"
        frappe.msgprint(_("Your course has been sent for review."))
```

The seller's existing Publish toggle then means "submit for review", and a `Marketplace Admin` approves it.

**To test in Phase 2:**
- That the Vue form displays the result correctly when the save returns `published = 0`.
- That `published_on` and the "quizzes without questions" warning do no harm, since both run before the hook.

---

## 4. Money flow

**Phase 1 uses the platform's one existing gateway, with payouts done by hand.** The `payments` app's Razorpay integration has no transfer or split-payment code, so automatic splits would be new code and can wait.

### Recording earnings: a sweep rather than a payment event

`doc_events` on `LMS Payment` **will not work** for this:

- `payment_received` is set with `frappe.db.set_value` (`payments.py:100`), and `update_payment_details` in `utils.py` also writes with `frappe.db.set_value`. These writes skip document events.
- Gateway rechecks can also complete a payment later, outside the original request (`queue_payment_recheck`).

Instead, a job in `scheduler_events` finds paid payments with no ledger row and creates one. The unique `payment` field makes it safe to re-run, and earnings appear within minutes.

```text
LMS Payment where payment_received = 1
              and payment_id is set
              and no Seller Ledger Entry exists
  -> seller = payment_for_document.seller
  -> gross = amount (after discount, before GST)
  -> commission = gross * rate, with the rate saved on the row
  -> status = Pending, available_on = today + hold days
```

### The manual payment gap

Instructors can record offline payments (`bulk_enrollment.py:324`). Those rows have `payment_received = 1` and no `payment_id`.

| Risk | Fix |
|---|---|
| Fake earnings if the sweep counted these rows | The sweep requires `payment_id` |
| Sellers enrolling paying students offline to avoid commission | `LMS Payment.before_insert` refuses `doc.flags.recorded_by_staff` unless the user is a marketplace admin |

A seller could still make a course free or use a 100% coupon and collect money elsewhere. That needs seller terms and monitoring, not code.

### Refunds

The LMS has no refund flow. The `payments` app does have `refund_payment` for Razorpay.

- **Phase 3:** an admin action refunds the payment, removes the enrolment and adds a reversal to the ledger.
- The hold period exists so refunds can come out of money not yet paid to the seller.

---

## 5. What hooks cannot do

| Limitation | Plan |
|---|---|
| The Vue app can't be changed through hooks | Use the www dashboard, sidebar item and existing screens first. Accept small Vue patches for polish, such as a seller name on course cards and "Submit for review" wording. |
| `frappe.get_all` ignores permission hooks, so hooks don't cover endpoints that use it | Audit endpoints (section 6) and wrap any that leak with `override_whitelisted_methods` |
| One `LMS Settings` for the whole site | Accepted: currency defaults, signup rules and templates stay platform-wide |
| GST is a fixed 18% on the course price, for India only (`utils.py:1338`) | Keep it for launch. Have an accountant confirm it fits a marketplace. |
| Automatic split payments | New API code in Phase 5 |

---

## 6. Isolation audit (Phase 2)

The LMS has **165** whitelisted endpoints, 26 of them open to guests, and `api.py` and `utils.py` alone contain **104** `get_all` calls. Hooks don't protect those calls, so this audit is required before any real seller joins.

Known items so far:

| Item | Finding | Action |
|---|---|---|
| `LMS Question` | Read is open to authoring roles by design (`has_authored_content_permission`) | Deny other sellers' questions with `has_permission` |
| `get_chart_details` | Returns site-wide counts | Decide whether this is acceptable; wrap it if not |
| `get_members` | Moderator only | Safe if sellers never hold Moderator |
| `get_all_users` | Limited to people in the discussion | Looks safe; confirm |
| Live class accounts, lesson files, email templates | Not reviewed yet | Include in the audit |

Add an automated test with two sellers: seller A must not be able to read or change seller B's drafts, students, payments, questions or earnings.

---

## 7. Phases

Estimates are rough guesses for one experienced Frappe developer.

| Phase | Delivers | Done when | Estimate |
|---|---|---|---|
| **0. Foundation** | New app, install in Docker, confirm hook behaviour, get the local fixes into git | App installs, and a test hook can deny access on top of an LMS rule | 2–3 days |
| **1. Sellers** | Seller DocType, Web Form, Workflow, role grant, `seller` field | An approved applicant can create a course that only they can edit | 1 week |
| **2. Review and isolation** | Review hook, Marketplace Admin role, audit fixes, two-seller tests | A seller cannot self-publish or reach another seller's data | 1–2 weeks |
| **3. Money** | Sweep, hold period, manual payment block, payouts, refunds, reports | A test Razorpay purchase produces the right ledger row and payout | 2 weeks |
| **4. Launch** | Dashboard, storefront, rebranding, seller terms, production deployment | A real seller can go from application to payout | 2–3 weeks |
| **5. Later** | Automatic split payments, seller teams, re-review of edited courses | Decided from real usage | Not estimated |

Roughly **7–10 weeks** to launch.

---

## 8. Decisions

Proposed defaults, used unless changed:

| Decision | Default |
|---|---|
| Commission | One platform-wide %, with a per-seller override |
| Hold period | 14 days |
| Currency | INR only at launch |
| Sellers | One login per seller; teams later |
| What sellers can sell | Courses first, then paid certificates and batches once the course flow works |
| Edits after approval | Go live without re-review, except that price changes are logged |
| Job board | Hidden at launch |

---

## 9. Outside the code: get professional advice

These are starting points to check, not legal or tax advice.

- **Holding sellers' money:** collecting payments for third parties may need a specific gateway arrangement. Ask your payment provider.
- **Indian tax:** marketplace operators may have GST TCS and income-tax TDS duties. Ask a chartered accountant, and check the same 18% GST treatment.
- **AGPL-3.0:** the LMS is AGPL. Ask a lawyer whether the new app must be offered under the same terms to users of the service. Assume it must.
- **Branding:** check Frappe's trademark rules before launch.
- **Seller terms:** content ownership, refunds, off-platform sales, takedowns.
- **Bank and tax data:** decide who can see it and how it is stored.
