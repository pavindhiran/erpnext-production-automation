frappe.ui.form.on("Job Card", {
    refresh(frm) {
        // ── Back to parent Work Order ──
        if (frm.doc.work_order) {
            frm.add_custom_button(__("← Back to Work Order"), () => {
                frappe.set_route("Form", "Work Order", frm.doc.work_order);
            });
        }

        // ── After marking Completed, offer jump back ──
        if (frm.doc.status === "Completed" && frm.doc.work_order) {
            frappe.show_alert({
                message: __("Job Card completed. Returning to Work Order…"),
                indicator: "green",
            }, 3);
            setTimeout(() => {
                frappe.set_route("Form", "Work Order", frm.doc.work_order);
            }, 1500);
        }
    },

    // ── When the Job Card is saved with Completed status, redirect ──
    after_save(frm) {
        if (frm.doc.status === "Completed" && frm.doc.work_order) {
            frappe.set_route("Form", "Work Order", frm.doc.work_order);
        }
    },
});