frappe.listview_settings["BOM"] = {
    onload(listview) {
        // Add a button per row: "View Work Order"
        listview.page.add_inner_button(__("View WO of selected"), () => {
            const selected = listview.get_checked_items();
            if (!selected.length) {
                frappe.msgprint("Select a BOM row first.");
                return;
            }
            const bom_name = selected[0].name;
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Work Order",
                    filters: { bom_no: bom_name, docstatus: ("<", 2) },
                    fields: ["name"],
                    limit_page_length: 50,
                },
                callback: (r) => {
                    const wos = r.message || [];
                    if (wos.length === 0) {
                        frappe.msgprint("No Work Order uses this BOM yet.");
                    } else if (wos.length === 1) {
                        frappe.set_route("Form", "Work Order", wos[0].name);
                    } else {
                        frappe.set_route("List", "Work Order", { bom_no: bom_name });
                    }
                },
            });
        });
    },
};