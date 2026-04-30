export function renderFaults(container, faults) {
    container.innerHTML = "<div class='title'>Faults Report (Generated via Celery)</div>";

    if (!faults || faults.length === 0) {
        container.innerHTML += "<div class='card'>No faults found.</div>";
        return;
    }

    faults.forEach(f => {
        const div = document.createElement("div");
        div.className = "card";
        // שמירה על הסטייל המקורי שלך
        div.style.borderLeft = "4px solid #38bdf8";
        div.style.marginBottom = "10px";
        div.style.padding = "15px";

        // תיקון: במקום להציג את f, אנחנו מציגים את השדות שבתוכו
        // השתמשתי ב-innerHTML כדי שזה ייראה מסודר
        div.innerHTML = `
            <div style="font-weight: bold; color: #1e293b; margin-bottom: 5px;">
                ${f.severity || 'Information'}
            </div>
            <div style="color: #475569;">
                ${f.description || 'No description available'}
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 10px;">
                ID: ${f.id} | Level: ${f.level || 'N/A'}
            </div>
        `;

        container.appendChild(div);
    });

    console.log("✅ FaultRenderer module executed successfully");
}