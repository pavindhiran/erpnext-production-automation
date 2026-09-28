import frappe


def execute(filters=None):
    columns = [
        {"label": "Work Order", "fieldname": "work_order", "fieldtype": "Link", "options": "Work Order", "width": 150},
        {"label": "Item", "fieldname": "production_item", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 70},
        {"label": "WO Status", "fieldname": "wo_status", "fieldtype": "Data", "width": 110},
        {"label": "Job Card", "fieldname": "job_card", "fieldtype": "Link", "options": "Job Card", "width": 150},
        {"label": "Operation", "fieldname": "operation", "fieldtype": "Data", "width": 120},
        {"label": "JC Status", "fieldname": "jc_status", "fieldtype": "Data", "width": 110},
    ]
    wo_filters = {"docstatus": 1}
    if filters and filters.get("work_order"):
        wo_filters["name"] = filters["work_order"]
    work_orders = frappe.get_list("Work Order", filters=wo_filters, fields=["name","production_item","qty","status"])
    data = []
    for wo in work_orders:
        jcs = frappe.get_list("Job Card", filters={"work_order": wo.name}, fields=["name","operation","status"])
        if not jcs:
            data.append({"work_order": wo.name, "production_item": wo.production_item, "qty": wo.qty, "wo_status": wo.status, "job_card": "", "operation": "", "jc_status": "No Job Cards"})
        else:
            for jc in jcs:
                data.append({"work_order": wo.name, "production_item": wo.production_item, "qty": wo.qty, "wo_status": wo.status, "job_card": jc.name, "operation": jc.operation, "jc_status": jc.status})
    return columns, data
