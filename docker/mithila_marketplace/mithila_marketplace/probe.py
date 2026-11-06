"""Phase 0: check how Frappe combines this app's hooks with the LMS's, on the version
actually installed. MARKETPLACE_PLAN.md depends on these answers.

The hooks below do nothing unless run() has set a flag in this process. run() rolls
everything back, so it changes no data.

  bench --site lms.localhost execute mithila_marketplace.probe.run
"""

import frappe

INSTRUCTOR = "priya.sharma@example.com"
OWN_COURSE = "python-programming-for-beginners"
OTHER_COURSE = "digital-marketing-fundamentals"


def course_has_permission(doc, ptype=None, user=None):
	"""Allows everything unless a probe names this course to deny."""
	return doc.name != frappe.flags.marketplace_probe_deny


def course_query_conditions(user=None, doctype=None):
	"""No condition unless a probe supplies one."""
	return frappe.flags.marketplace_probe_query or ""


def course_validate(doc, method=None):
	"""Records what the LMS controller left on the document, if a probe is listening."""
	if frappe.flags.marketplace_probe_seen is not None:
		frappe.flags.marketplace_probe_seen.update(status=doc.status, published=doc.published)
		doc.status = "Under Review"
		doc.published = 0


def _reset():
	frappe.flags.marketplace_probe_deny = None
	frappe.flags.marketplace_probe_query = None
	frappe.flags.marketplace_probe_seen = None


def _listed(user):
	frappe.set_user(user)
	return set(frappe.get_list("LMS Course", pluck="name", limit_page_length=0))


def run():
	results = []

	def check(name, passed, detail=""):
		results.append(passed)
		print(f"{'PASS' if passed else 'FAIL'}  {name}{f'  [{detail}]' if detail else ''}")

	_reset()
	try:
		print(f"Frappe version: {frappe.__version__}")

		for hook, label in (("has_permission", "has_permission"), ("permission_query_conditions", "query")):
			registered = frappe.get_hooks(hook).get("LMS Course", [])
			apps = {path.split(".")[0] for path in registered}
			check(f"{label} hooks from both apps are registered", {"lms", "mithila_marketplace"} <= apps)

		# has_permission: this app can take away access the LMS would give.
		frappe.set_user(INSTRUCTOR)
		can_write = lambda course: frappe.has_permission("LMS Course", "write", doc=course, user=INSTRUCTOR)
		check("instructor can write own course by default", bool(can_write(OWN_COURSE)))
		frappe.flags.marketplace_probe_deny = OWN_COURSE
		check("our has_permission hook can deny on top of LMS", not can_write(OWN_COURSE))
		frappe.flags.marketplace_probe_deny = None

		# has_permission: returning True must not override a denial from the LMS.
		check("our True does not override the LMS denying another course", not can_write(OTHER_COURSE))

		# Query conditions: both apps' conditions must apply (AND, not OR).
		base = _listed(INSTRUCTOR)
		unpublished = set(frappe.get_all("LMS Course", {"published": 0}, pluck="name"))
		check("base list excludes unpublished courses", bool(base) and not (base & unpublished), f"{len(base)} listed")

		frappe.flags.marketplace_probe_query = "`tabLMS Course`.`name` is not null"
		widened = _listed(INSTRUCTOR)
		if unpublished:
			check("a condition matching everything does not widen the LMS rule (AND)", widened == base)
		else:
			check("AND check needs an unpublished course", False, "none on this site")

		frappe.flags.marketplace_probe_query = f"`tabLMS Course`.`name` != {frappe.db.escape(OWN_COURSE)}"
		narrowed = _listed(INSTRUCTOR)
		check("our condition can narrow the list", narrowed == base - {OWN_COURSE})

		# frappe.get_all ignores hooks: why the plan needs an endpoint audit.
		every = frappe.get_all("LMS Course", pluck="name")
		check("frappe.get_all ignores our condition", OWN_COURSE in every)
		frappe.flags.marketplace_probe_query = None

		# Document events: the review hook needs to run after the controller and have the last word.
		frappe.set_user("Administrator")
		doc = frappe.get_doc("LMS Course", OWN_COURSE)
		doc.published = 1
		doc.status = "In Progress"
		frappe.flags.marketplace_probe_seen = {}
		doc.run_method("validate")
		seen = frappe.flags.marketplace_probe_seen
		frappe.flags.marketplace_probe_seen = None
		check("our validate runs after the LMS controller", seen.get("status") == "Approved", str(seen))
		check(
			"our validate has the last word",
			doc.status == "Under Review" and not doc.published,
			f"status={doc.status} published={doc.published}",
		)
	finally:
		_reset()
		frappe.set_user("Administrator")
		frappe.db.rollback()

	print(f"{sum(results)}/{len(results)} checks passed")
	if not all(results):
		frappe.throw("Marketplace hook checks failed")
	print("PROBE_DONE")
