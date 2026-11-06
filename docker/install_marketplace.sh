#!/bin/bash
# Installs the local mithila_marketplace app into the bench. Safe to re-run.
# The source lives in docker/mithila_marketplace, visible in the container at /workspace.
#
# On a bench that is already running, restart the container straight after this
# ("docker restart lms-frappe-1"). Until then the running processes can't import the
# new app and every page returns a 500.
set -euo pipefail

SITE="${1:-lms.localhost}"
APP=mithila_marketplace
cd /home/frappe/frappe-bench

ln -sfn "/workspace/$APP" "apps/$APP"
uv pip install --quiet -e "apps/$APP" --python env/bin/python

# sites/apps.txt may not end in a newline.
if ! grep -qx "$APP" sites/apps.txt; then
	[ -z "$(tail -c1 sites/apps.txt)" ] || echo >> sites/apps.txt
	echo "$APP" >> sites/apps.txt
fi

bench --site "$SITE" install-app "$APP"
bench --site "$SITE" clear-cache
echo INSTALL_DONE
