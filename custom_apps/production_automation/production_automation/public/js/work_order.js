frappe.ui.form.on("Work Order", {
    refresh(frm) {
        // ── Link to Job Cards ──
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("View Job Cards"), () => {
                frappe.set_route("List", "Job Card", { work_order: frm.doc.name });
            });
        }

        // ── The two automation buttons ──
        if (frm.doc.docstatus !== 1) return;
        if (frm.doc.status === "Completed") return;

        frm.add_custom_button(__("▶ Start Production"), () => {
            frappe.confirm("Start production? Creates Job Cards and transfers materials.", () => {
                frm.call("start_production").then(() => {
                    frappe.show_alert({ message: "Production started", indicator: "green" });
                    frm.reload_doc();
                });
            });
        }, __("Actions")).addClass("btn-primary");

        frm.add_custom_button(__("✔ Complete Production"), () => {
            frappe.confirm("Complete production? All Job Cards must be finished first.", () => {
                frm.call("complete_production").then(() => {
                    frappe.show_alert({ message: "Production completed", indicator: "green" });
                    frm.reload_doc();
                    // ── After complete, jump to the report ──
                    setTimeout(() => {
                        frappe.set_route("query-report", "Production Status");
                    }, 800);
                });
            });
        }, __("Actions"));
    },
});