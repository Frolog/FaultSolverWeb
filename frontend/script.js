const API = `${window.location.origin}/api`;
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
 * טיפול בבקשת תקלות דרך Celery - בדיקה כל שנייה והצגה ב-Content
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

                // --- תוספת אבחון ---
                console.log("🎯 Celery Task Success!");
                console.log("📦 Result from API:", data.result);
                // -------------------

                try {
                    const { renderFaults } = await import('./modules/faultRenderer.js');

                    // בדיקה אם ה-result בכלל מכיל נתונים לפני ששולחים לרינדור
                    if (data.result && data.result.length > 0) {
                        renderFaults(content, data.result);
                    } else {
                        console.warn("⚠️ המשימה הצליחה אך ה-result ריק. בודק אם ה-DB מכיל נתונים ל-ID הזה.");
                        content.innerHTML = "<div class='card'>לא נמצאו תקלות במערכת עבור פריט זה.</div>";
                    }
                } catch (importErr) {
                    console.error("❌ Import Error:", importErr);
                    content.innerHTML = "<div class='card'>שגיאה בטעינת מודול התצוגה</div>";
                }
            } else if (data.state === 'FAILURE' || data.state === 'REVOKED') {
                clearInterval(checkStatus);
                console.error("❌ Task Failed/Revoked. Detail:", data);
                content.innerHTML = "<div class='card'>שגיאה בעיבוד המשימה בשרת</div>";
            }
        }, 1000);
    } catch (err) {
        content.innerHTML = "<div class='card'>שגיאה בתקשורת עם השרת</div>";
    }
}

// בתוך פונקציית ה-toggle או ה-click handler של העץ:
function toggleNode(header, content) {
    const isExpanded = content.style.display !== 'none';
    const icon = header.querySelector('.tree-icon');

    if (isExpanded) {
        // סגירת ענף
        content.style.display = 'none';
        if (icon) {
            icon.classList.remove('bi-dash-square');
            icon.classList.add('bi-plus-square');
        }
    } else {
        // פתיחת ענף
        content.style.display = 'block';
        if (icon) {
            icon.classList.remove('bi-plus-square');
            icon.classList.add('bi-dash-square');
        }
    }
}

/**
 * פונקציה ליצירת צומת בעץ (פרויקט/מערכת/תת-מכלול/תקלה)
 */
function addNode(parent, text, level, onClick) {
    const wrapper = document.createElement("div");
    wrapper.className = "node-wrapper";

    const div = document.createElement("div");
    div.className = "node";
    div.style.paddingRight = (level * 20) + "px"; // RTL padding
    div.innerHTML = text; // שימוש ב-innerHTML כדי לאפשר תגיות SPAN לצבעים

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

        childrenContainer = document.createElement("div");
        childrenContainer.className = "children-container";
        wrapper.appendChild(childrenContainer);

        div.classList.add("expanded");

        // הפעלת הפונקציה שנשלחה רק אם היא קיימת
        if (onClick) {
            await onClick(childrenContainer);
        }
        expanded = true;
    };
}

/**
 * טעינה ראשונית של העץ (רמת פרויקטים)
 */
async function load() {
    if (!tree) return;

    tree.innerHTML = "<p style='padding:10px; color: #aaa;'>טוען פרויקטים...</p>";

    try {
        const projects = await fetchJSON(`${API}/projects`);
        tree.innerHTML = "";

        if (projects.length === 0) {
            tree.innerHTML = "<p style='padding:10px'>לא נמצאו פרויקטים.</p>";
            return;
        }

        projects.forEach(p => {
            addNode(tree, `📁 [ID: ${p.id}] ${p.name}`, 0, async (cont) => {
                if (cont.innerHTML !== "") return;
                cont.innerHTML = "<li style='list-style:none; color: #888; padding-right:20px'>⌛ טוען מערכות...</li>";

                try {
                    const systems = await fetchJSON(`${API}/systems/${p.id}`);
                    cont.innerHTML = "";

                    if (systems.length === 0) {
                        addNode(cont, "❌ לא נמצאו מערכות", 1);
                        return;
                    }

                    systems.forEach(s => {
                        addNode(cont, "🧩 " + s.name, 1, async (subCont) => {
                            if (subCont.innerHTML !== "") return;
                            subCont.innerHTML = "<li style='list-style:none; color: #888; padding-right:40px'>⌛ טוען תתי-מכלולים...</li>";

                            const subs = await fetchJSON(`${API}/subassemblies/${s.id}`);
                            subCont.innerHTML = "";

                            if (subs.length === 0) {
                                addNode(subCont, "ℹ️ אין תתי-מכלולים", 2);
                                return;
                            }

                            subs.forEach(sub => {
                                // רמה 2: תתי-מכלולים - כאן מתבצע החיבור ל-Celery ולתצוגת התקלות
                                addNode(subCont, "🔧 " + sub.name, 2, async (faultCont) => {
                                    // 1. עדכון הצד השמאלי (כרטיס Celery)
                                    handleFaultsRequest(sub.id);

                                    // 2. עדכון העץ (רמה רביעית - תקלות)
                                    if (faultCont.innerHTML !== "") return;
                                    faultCont.innerHTML = "<li style='list-style:none; color: #888; padding-right:60px'>⌛ בודק תקלות...</li>";

                                    try {
                                        // קריאה לקבלת התקלות עבור העץ
                                        const faults = await fetchJSON(`${API}/faults/async/subassembly/${sub.id}`);
                                        faultCont.innerHTML = "";

                                        // אם ה-API מחזיר task_id (אסינכרוני), נחכה לתוצאה או נשתמש בנתוני דמו 
                                        // הערה: מומלץ שה-Route הזה יחזיר JSON ישיר לעץ לביצועים מהירים
                                        if (!Array.isArray(faults) || faults.length === 0) {
                                            addNode(faultCont, "✅ אין תקלות רשומות", 3);
                                            return;
                                        }

                                        faults.forEach(f => {
                                            const color = f.severity === 'High' ? '#ff4444' : '#ffbb33';
                                            const faultLabel = `⚠️ <span style="color:${color}">[${f.severity}]</span> ${f.description}`;
                                            addNode(faultCont, faultLabel, 3);
                                        });
                                    } catch (err) {
                                        faultCont.innerHTML = "<li style='color:red; padding-right:60px'>שגיאה בטעינת תקלות</li>";
                                    }
                                });
                            });
                        });
                    });
                } catch (err) {
                    cont.innerHTML = "<li style='color:red; padding-right:20px'>שגיאה בטעינת מערכות</li>";
                }
            });
        });
    } catch (err) {
        tree.innerHTML = "<p style='padding:10px; color:red'>שגיאה בטעינת נתונים מהשרת</p>";
    }
}

// הרצה ראשונית
load();