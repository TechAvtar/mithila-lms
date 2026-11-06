from . import __version__ as app_version  # noqa: F401

app_name = "mithila_marketplace"
app_title = "Mithila Marketplace"
app_publisher = "TechAvtar"
app_description = "Multi-seller marketplace for Frappe Learning"
app_email = ""
app_license = "AGPL-3.0"
required_apps = ["frappe/lms"]

# Phase 0 probes. Each one does nothing unless mithila_marketplace.probe.run has set
# its flag for the current process, so normal requests are unaffected.
has_permission = {
	"LMS Course": "mithila_marketplace.probe.course_has_permission",
}

permission_query_conditions = {
	"LMS Course": "mithila_marketplace.probe.course_query_conditions",
}

doc_events = {
	"LMS Course": {
		"validate": "mithila_marketplace.probe.course_validate",
	},
}
