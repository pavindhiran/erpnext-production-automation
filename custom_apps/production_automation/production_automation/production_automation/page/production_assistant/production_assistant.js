frappe.pages["production-assistant"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "Production Assistant",
        single_column: true,
    });

    $(page.body).html(`
        <div style="padding:20px; max-width:900px;">
            <h3>Ask about production</h3>
            <p style="color:#666;">
                Try: "Show job cards that are not completed" &middot;
                "Show completed job cards" &middot;
                "Show work orders without a job card" &middot;
                "Which work orders are started but their job cards are not completed?" &middot;
                "Which work orders are pending?" &middot;
                "Show the production status of MFG-WO-2026-00001"
            </p>
            <input id="pa-query" class="form-control" placeholder="Type your question..." style="margin-bottom:10px;">
            <button id="pa-ask" class="btn btn-primary btn-sm">Ask</button>
            <div id="pa-result" style="margin-top:20px;"></div>
        </div>
    `);

    const ask = () => {
        const q = $("#pa-query").val();
        if (!q) return;
        $("#pa-result").html("<em>Searching…</em>");
        frappe.call({
            method: "production_automation.api.ask_production_query",
            args: { user_query: q },
            callback: (r) => render(r.message),
        });
    };

    $("#pa-ask").on("click", ask);
    $("#pa-query").on("keypress", (e) => { if (e.which === 13) ask(); });

    function render(msg) {
        let html = `<h4>${frappe.utils.escape_html(msg.message || "")}</h4>`;
        const data = msg.data || [];
        if (data.length) {
            const keys = Object.keys(data[0]);
            html += '<table class="table table-bordered table-sm"><thead><tr>';
            keys.forEach((k) => (html += `<th>${frappe.utils.escape_html(k)}</th>`));
            html += "</tr></thead><tbody>";
            data.forEach((row) => {
                html += "<tr>";
                keys.forEach((k) => (html += `<td>${frappe.utils.escape_html(row[k] ?? "")}</td>`));
                html += "</tr>";
            });
            html += "</tbody></table>";
        }
        $("#pa-result").html(html);
    }
};