const API = "http://127.0.0.1:5000";

const tree = document.getElementById("tree");
const content = document.getElementById("content");

async function fetchJSON(url) {
    const res = await fetch(url);
    return await res.json();
}

function addNode(text, level, onClick) {
    const div = document.createElement("div");
    div.className = "node";
    div.style.paddingLeft = (level * 15) + "px";
    div.innerText = text;

    div.onclick = onClick;

    tree.appendChild(div);
}

// Load projects first
async function load() {
    const projects = await fetchJSON(`${API}/projects`);

    projects.forEach(p => {

        addNode("📁 " + p.name, 0, async () => {

            const systems = await fetchJSON(`${API}/systems/${p.name}`);

            systems.forEach(s => {

                addNode("🧩 " + s.name, 1, async () => {

                    const subs = await fetchJSON(`${API}/subassemblies/${p.name}/${s.name}`);

                    subs.forEach(sub => {

                        addNode("🔧 " + sub.name, 2, async () => {

                            const faults = await fetchJSON(`${API}/faults/${sub.name}`);

                            showFaults(faults);

                        });

                    });

                });

            });

        });

    });
}

function showFaults(faults) {
    content.innerHTML = "<div class='title'>Faults</div>";

    faults.forEach(f => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerText = f;
        content.appendChild(div);
    });
}

load();