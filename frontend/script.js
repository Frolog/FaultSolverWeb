async function fetchJSON(url) {
    const res = await fetch(url);
    return await res.json();
}

const projectSelect = document.getElementById("project");
const systemSelect = document.getElementById("system");
const subSelect = document.getElementById("sub");
const cardSelect = document.getElementById("card");
const faultSelect = document.getElementById("fault");
const stepsList = document.getElementById("steps_list");

// Load projects
fetchJSON("http://127.0.0.1:5000/projects").then(data => {
    data.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.text = p.name;
        projectSelect.add(option);
    });
});

// Project → System
projectSelect.addEventListener("change", async () => {
    const projectId = projectSelect.value;
    systemSelect.innerHTML = ""; subSelect.innerHTML = ""; cardSelect.innerHTML = ""; faultSelect.innerHTML = ""; stepsList.innerHTML = "";
    const systems = await fetchJSON(`http://127.0.0.1:5000/systems/${projectId}`);
    systems.forEach(s => {
        const option = document.createElement("option");
        option.value = s.id; option.text = s.name;
        systemSelect.add(option);
    });
    systemSelect.disabled = false;
});

// System → Subassembly
systemSelect.addEventListener("change", async () => {
    const systemId = systemSelect.value;
    subSelect.innerHTML = ""; cardSelect.innerHTML = ""; faultSelect.innerHTML = ""; stepsList.innerHTML = "";
    const subs = await fetchJSON(`http://127.0.0.1:5000/subassemblies/${systemId}`);
    subs.forEach(s => { const option = document.createElement("option"); option.value = s.id; option.text = s.name; subSelect.add(option); });
    subSelect.disabled = false;
});

// Subassembly → Card
subSelect.addEventListener("change", async () => {
    const subId = subSelect.value;
    cardSelect.innerHTML = ""; faultSelect.innerHTML = ""; stepsList.innerHTML = "";
    const cards = await fetchJSON(`http://127.0.0.1:5000/cards/${subId}`);
    cards.forEach(c => { const option = document.createElement("option"); option.value = c.id; option.text = c.name; cardSelect.add(option); });
    cardSelect.disabled = false;
});

// Card → Fault
cardSelect.addEventListener("change", async () => {
    const cardId = cardSelect.value;
    faultSelect.innerHTML = ""; stepsList.innerHTML = "";
    const faults = await fetchJSON(`http://127.0.0.1:5000/faults/card/${cardId}`);
    faults.forEach(f => { const option = document.createElement("option"); option.value = f.id; option.text = f.description; faultSelect.add(option); });
    faultSelect.disabled = false;
});

// Fault → Steps
faultSelect.addEventListener("change", async () => {
    const faultId = faultSelect.value;
    stepsList.innerHTML = "";
    const steps = await fetchJSON(`http://127.0.0.1:5000/steps/${faultId}`);
    steps.forEach(s => {
        const li = document.createElement("li");
        li.textContent = `${s.step_number}: ${s.step} (${s.explanation})`;
        stepsList.appendChild(li);
    });
});