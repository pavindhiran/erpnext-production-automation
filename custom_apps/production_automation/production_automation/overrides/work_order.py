import frappe
from erpnext.manufacturing.doctype.work_order.work_order import (
    WorkOrder,
    make_stock_entry as make_stock_entry_from_wo,
)


class CustomWorkOrder(WorkOrder):
    """Adds one-click Start / Complete automation to Work Order."""

    @frappe.whitelist()
    def start_production(self):
        # 1) Create Job Cards if none
        if not frappe.db.exists("Job Card", {"work_order": self.name}):
            self.create_job_card()

        # 2) Material Transfer for Manufacture
        already = frappe.db.exists(
            "Stock Entry",
            {
                "work_order": self.name,
                "purpose": "Material Transfer for Manufacture",
                "docstatus": ("<", 2),
            },
        )
        if not already:
            se_dict = make_stock_entry_from_wo(self.name, "Material Transfer for Manufacture")
            se = frappe.get_doc(se_dict)
            se.insert(ignore_permissions=True)
            se.submit()

        self.db_set("status", "In Process")
        frappe.db.commit()
        return True

    @frappe.whitelist()
    def complete_production(self):
        # 1) Ensure all Job Cards are done
        pending = frappe.get_all(
            "Job Card",
            filters={"work_order": self.name, "status": ("!=", "Completed")},
            pluck="name",
        )
        if pending:
            frappe.throw("Cannot complete. Pending Job Cards: " + ", ".join(pending))

        # 2) Manufacture Stock Entry
        already = frappe.db.exists(
            "Stock Entry",
            {
                "work_order": self.name,
                "purpose": "Manufacture",
                "docstatus": ("<", 2),
            },
        )
        if not already:
            se_dict = make_stock_entry_from_wo(self.name, "Manufacture")
            se = frappe.get_doc(se_dict)
            se.insert(ignore_permissions=True)
            se.submit()

        self.db_set("status", "Completed")
        frappe.db.commit()
        return True