export function renderFaults(container, faults) {
    container.innerHTML = "<div class='title'>Faults Report (Generated via Celery)</div>";
    
    if (!faults || faults.length === 0) {
        container.innerHTML += "<div class='card'>No faults found.</div>";
        return;
    }

    faults.forEach(f => {
        const div = document.createElement("div");
        div.className = "card";
        // הוספת סטייל קטן כדי לזהות שזה הגיע מהמודול החדש
        div.style.borderLeft = "4px solid #38bdf8"; 
        div.innerText = f;
        container.appendדChild(div);
    });

    console.log("✅ FaultRenderer module executed");
}