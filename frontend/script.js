console.log("🚀 script.js loaded");

const API = "http://127.0.0.1:5000";

const tree = document.getElementById("tree");
const content = document.getElementById("content");

async function fetchJSON(url) {
    const res = await fetch(url);
    return await res.json();
}

function addNode(parent, text, level, onClick) {
    const wrapper = document.createElement("div");

    const div = document.createElement("div");
    div.className = "node";
    div.style.paddingLeft = (level * 15) + "px";
    div.innerText = text;

    wrapper.appendChild(div);
    parent.appendChild(wrapper);

    let expanded = false;
    let childrenContainer = null;

    div.onclick = async () => {
        if (expanded) {
            childrenContainer.remove();
            expanded = false;
            return;
        }

        childrenContainer = document.createElement("div");
        wrapper.appendChild(childrenContainer);

        await onClick(childrenContainer);

        expanded = true;
    };
}

// Load projects
async function load() {
    console.log("📡 load() started");

    tree.innerHTML = "";

    const projects = await fetchJSON(`${API}/projects`);
    console.log("📁 projects:", projects);

    projects.forEach(p => {

        addNode(tree, "📁 " + p.name, 0, async (projectContainer) => {

            const systems = await fetchJSON(`${API}/systems/${p.id}`);

            systems.forEach(s => {

                addNode(projectContainer, "🧩 " + s.name, 1, async (systemContainer) => {

                    const subs = await fetchJSON(`${API}/subassemblies/${s.id}`);

                    subs.forEach(sub => {

                        addNode(systemContainer, "🔧 " + sub.name, 2, async () => {

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