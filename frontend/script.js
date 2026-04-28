const API = window.location.origin; // גמיש יותר לשינויי פורטים
const tree = document.getElementById("tree");
const content = document.getElementById("content");

/**
 * פונקציית עזר למשיכת JSON מהשרת
 */
async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error("Fetch error:", e);
        return [];
    }
}

/**
 * טיפול בבקשת תקלות דרך Celery - בדיקה כל שנייה
 */
async function handleFaultsRequest(subId) {
    content.innerHTML = `
        <div class='card'>
            <div class='loading-spinner'></div>
            <p style="text-align:center">מעבד נתונים ב-Celery...</p>
            <p style="text-align:center; font-size: 0.8em; color: #888;">(בדיקת סטטוס כל שנייה)</p>
        </div>`;

    try {
        // שליחת המשימה ל-Worker
        const res = await fetch(`${API}/faults/async/subassembly/${subId}`);
        const { task_id } = await res.json();

        // מנגנון בדיקה כל שנייה (Polling)
        const checkStatus = setInterval(async () => {
            const statusRes = await fetch(`${API}/tasks/status/${task_id}`);
            const data = await statusRes.json();

            console.log(`Task ${task_id} state: ${data.state}`);

            if (data.state === 'SUCCESS') {
                clearInterval(checkStatus);
                // ייבוא דינמי של המרנדר והצגת התוצאות
                try {
                    const { renderFaults } = await import('./modules/faultRenderer.js');
                    renderFaults(content, data.result);
                } catch (importErr) {
                    content.innerHTML = "<div class='card'>שגיאה בטעינת מודול התצוגה</div>";
                }
            } else if (data.state === 'FAILURE' || data.state === 'REVOKED') {
                clearInterval(checkStatus);
                content.innerHTML = "<div class='card'>שגיאה בעיבוד המשימה בשרת</div>";
            }
        }, 1000); // הפנייה כל שנייה
    } catch (err) {
        content.innerHTML = "<div class='card'>שגיאה בתקשורת עם השרת</div>";
    }
}

/**
 * פונקציה ליצירת צומת בעץ (פרויקט/מערכת/תת-מכלול)
 * onClick יופעל רק כשהצומת נפתח
 */
function addNode(parent, text, level, onClick) {
    const wrapper = document.createElement("div");
    wrapper.className = "node-wrapper";

    const div = document.createElement("div");
    div.className = "node";
    div.style.paddingRight = (level * 20) + "px"; // שימוש ב-Right בגלל RTL
    div.innerText = text;
    
    wrapper.appendChild(div);
    parent.appendChild(wrapper);

    let expanded = false;
    let childrenContainer = null;

    div.onclick = async (e) => {
        e.stopPropagation();
        
        if (expanded) {
            if (childrenContainer) childrenContainer.remove();
            expanded = false;
            div.classList.remove("expanded");
            return;
        }

        // יצירת מיכל לילדים וטעינת נתונים רק עכשיו
        childrenContainer = document.createElement("div");
        childrenContainer.className = "children-container";
        wrapper.appendChild(childrenContainer);
        
        div.classList.add("expanded");
        await onClick(childrenContainer);
        expanded = true;
    };
}

/**
 * טעינה ראשונית של העץ (רמת פרויקטים)
 */
async function load() {
    if (!tree) return;
    tree.innerHTML = "<p style='padding:10px'>טוען פרויקטים...</p>";
    
    const projects = await fetchJSON(`${API}/projects`);
    tree.innerHTML = ""; // ניקוי הודעת טעינה

    projects.forEach(p => {
        // רמה 0: פרויקטים
        addNode(tree, "📁 " + p.name, 0, async (cont) => {
            const systems = await fetchJSON(`${API}/systems/${p.id}`);
            
            systems.forEach(s => {
                // רמה 1: מערכות
                addNode(cont, "🧩 " + s.name, 1, async (subCont) => {
                    const subs = await fetchJSON(`${API}/subassemblies/${s.id}`);
                    
                    subs.forEach(sub => {
                        // רמה 2: תתי-מכלולים (לחיצה אחרונה מפעילה Celery)
                        addNode(subCont, "🔧 " + sub.name, 2, async () => {
                            handleFaultsRequest(sub.id);
                        });
                    });
                });
            });
        });
    });
}

// הפעלה
load();