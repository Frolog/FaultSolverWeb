console.log("🚀 script.js loaded");
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
    console.log("📡 load() started");
    const projects = await fetchJSON(`${API}/projects`);
    console.log("📁 projects:", projects);
    
    projects.forEach(p => {

        addNode("📁 " + p.name, 0, async () => {

            // ✅ FIX: use ID
            const systems = await fetchJSON(`${API}/systems/${p.id}`);

            systems.forEach(s => {

                addNode("🧩 " + s.name, 1, async () => {

                    // ✅ FIX: use system ID
                    const subs = await fetchJSON(`${API}/subassemblies/${s.id}`);

                    subs.forEach(sub => {

                        addNode("🔧 " + sub.name, 2, async () => {

                            // ✅ FIX: use subassembly ID
                            const faults = await fetchJSON(`${API}/faults/${sub.id}`);

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