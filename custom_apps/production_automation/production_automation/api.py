import re
import frappe


@frappe.whitelist()
def ask_production_query(user_query: str):
    """Parse a natural-language production query and return matching rows."""
    q = (user_query or "").lower().strip()

    if not q:
        return {"message": "Please type a question.", "data": []}

    wo_match = re.search(r"(mfg-wo-\d{4}-\d+|wo-\d+)", q, re.IGNORECASE)

    # 1) "Show job cards that are not completed"
    if "job card" in q and ("not completed" in q or "pending" in q or "incomplete" in q):
        return _job_cards(status_not="Completed")

    # 2) "Show completed job cards"
    if "job card" in q and "completed" in q:
        return _job_cards(status="Completed")

    # 3) "Show work orders without a job card"
    if "work order" in q and "without" in q and "job card" in q:
        return _work_orders_without_job_cards()

    # 4) "Which work orders are started but their job cards are not completed?"
    if "started" in q and "job card" in q and ("not completed" in q or "pending" in q):
        return _started_wo_with_pending_jc()

    # 5) "Show the production status of WO-0001" / "MFG-WO-2026-00001"
    if wo_match and ("status" in q or "production" in q):
        return _work_order_status(wo_match.group(0))

    # 6) "Which work orders are pending?"
    if "work order" in q and ("pending" in q or "open" in q or "not started" in q):
        return _pending_work_orders()

    return {
        "message": "I couldn't understand. Try: 'Show job cards that are not completed'.",
        "data": [],
    }


def _job_cards(status=None, status_not=None):
    filters = {}
    if status:
        filters["status"] = status
    if status_not:
        filters["status"] = ("!=", status_not)
    rows = frappe.get_list(
        "Job Card",
        filters=filters,
        fields=["name", "work_order", "operation", "status", "for_quantity"],
        limit_page_length=50,
    )
    return {"message": f"{len(rows)} Job Card(s) found.", "data": rows}


def _pending_work_orders():
    rows = frappe.get_list(
        "Work Order",
        filters={"status": ("not in", ["Completed", "Cancelled", "Closed"])},
        fields=["name", "production_item", "qty", "status"],
        limit_page_length=50,
    )
    return {"message": f"{len(rows)} pending Work Order(s).", "data": rows}


def _work_orders_without_job_cards():
    wos = frappe.get_list("Work Order", filters={"docstatus": 1}, pluck="name")
    with_jc = set(
        frappe.get_list("Job Card", filters={"work_order": ("in", wos)}, pluck="work_order")
    )
    missing = [w for w in wos if w not in with_jc]
    if not missing:
        return {"message": "Every Work Order has a Job Card.", "data": []}
    rows = frappe.get_list(
        "Work Order",
        filters={"name": ("in", missing)},
        fields=["name", "production_item", "qty", "status"],
    )
    return {"message": f"{len(rows)} Work Order(s) without Job Cards.", "data": rows}


def _started_wo_with_pending_jc():
    started = frappe.get_list("Work Order", filters={"status": "In Process"}, pluck="name")
    if not started:
        return {"message": "No Work Orders are 'In Process'.", "data": []}
    rows = frappe.get_list(
        "Job Card",
        filters={"work_order": ("in", started), "status": ("!=", "Completed")},
        fields=["name", "work_order", "operation", "status"],
    )
    return {"message": f"{len(rows)} incomplete Job Card(s).", "data": rows}


def _work_order_status(wo_name):
    if not frappe.db.exists("Work Order", wo_name):
        return {"message": f"{wo_name} not found.", "data": []}
    wo = frappe.get_doc("Work Order", wo_name)
    jcs = frappe.get_list(
        "Job Card",
        filters={"work_order": wo_name},
        fields=["name", "operation", "status"],
    )
    data = [
        {
            "work_order": wo.name,
            "item": wo.production_item,
            "qty": wo.qty,
            "wo_status": wo.status,
        }
    ]
    for j in jcs:
        data.append(
            {"work_order": j.name, "item": j.operation, "qty": "", "wo_status": j.status}
        )
    return {"message": f"Status for {wo_name}: {wo.status}", "data": data}