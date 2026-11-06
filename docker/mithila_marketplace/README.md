# Mithila Marketplace

Multi-seller marketplace for Frappe Learning, built as a separate Frappe app so that
`lms` stays unmodified. See `MARKETPLACE_PLAN.md` in the repository root.

**Status:** Phase 0. The app contains only the hook behaviour checks. Its hooks do
nothing unless `mithila_marketplace.probe.run` is executing.

## Install (local Docker setup)

Run from the `docker` folder:

```bash
docker exec -w /home/frappe/frappe-bench lms-frappe-1 bash -lc 'bash /workspace/install_marketplace.sh'
docker restart lms-frappe-1
```

The restart is required on a running bench. Until it happens, every page returns a 500.

## Run the hook checks

They change nothing: all work is rolled back.

```bash
docker exec -w /home/frappe/frappe-bench lms-frappe-1 bash -lc 'bench --site lms.localhost execute mithila_marketplace.probe.run'
```

The checks rely on the sample users from `seed_client_demo.py`.
