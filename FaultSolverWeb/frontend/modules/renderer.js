export function advancedRender(container, data) {
    // כאן יכול להיות קוד מורכב מאוד, גרפים או טבלאות
    console.log("Rendering data dynamically...");
    container.innerHTML += `<div class='card'>Total Faults Found: ${data.length}</div>`;
}