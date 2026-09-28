app_name = "production_automation"
app_title = "Production Automation"
app_publisher = "Pavindhiran"
app_description = "Custom production flow automation"
app_email = "you@example.com"
app_license = "MIT"


# Override the Work Order controller
override_doctype_class = {
    "Work Order": "production_automation.overrides.work_order.CustomWorkOrder"
}

doctype_js = {
    "BOM":       "public/js/bom.js",
    "Work Order": "public/js/work_order.js",
    "Job Card":  "public/js/job_card.js",
}
doctype_list_js = {
    "BOM": "public/js/bom_list.js",
}