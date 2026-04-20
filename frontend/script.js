const API = "http://127.0.0.1:5000";
const tree = document.getElementById("tree");
const content = document.getElementById("content");

async function fetchJSON(url) {
    const res = await fetch(url);
    return await res.json();
}

async function handleFaultsRequest(subId) {
    content.innerHTML = `
        <div class='card'>
            <div class='loading-spinner'></div>
            <p style="text-align:center">מעבד נתונים ב-Celery...</p>
        </div>`;

    try {
        const res = await fetch(`${API}/faults/async/subassembly/${subId}`);
        const { task_id } = await res.json();

        const checkStatus = setInterval(async () => {
            const statusRes = await fetch(`${API}/tasks/status/${task_id}`);
            const data = await statusRes.json();

            if (data.state === 'SUCCESS') {
                clearInterval(checkStatus);
                // DYNAMIC IMPORT
                const { renderFaults } = await import('./modules/faultRenderer.js');
                renderFaults(content, data.result);
            } else if (data.state === 'FAILURE') {
                clearInterval(checkStatus);
                content.innerHTML = "<div class='card'>שגיאה בעיבוד המשימה</div>";
            }
        }, 1000);
    } catch (err) {
        content.innerHTML = "<div class='card'>שגיאה בתקשורת עם השרת</div>";
    }
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

async function load() {
    tree.innerHTML = "";
    const projects = await fetchJSON(`${API}/projects`);
    projects.forEach(p => {
        addNode(tree, "📁 " + p.name, 0, async (cont) => {
            const systems = await fetchJSON(`${API}/systems/${p.id}`);
            systems.forEach(s => {
                addNode(cont, "🧩 " + s.name, 1, async (subCont) => {
                    const subs = await fetchJSON(`${API}/subassemblies/${s.id}`);
                    subs.forEach(sub => {
                        addNode(subCont, "🔧 " + sub.name, 2, async () => {
                            handleFaultsRequest(sub.id);
                        });
                    });
                });
            });
        });
    });
}

load();