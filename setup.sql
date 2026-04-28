-- יצירת טבלת פרויקטים
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- יצירת טבלת מערכות
CREATE TABLE systems (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL
);

-- יצירת טבלת תת-מכלולים (Subassemblies)
CREATE TABLE subassemblies (
    id SERIAL PRIMARY KEY,
    system_id INTEGER REFERENCES systems(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL
);

-- הכנסת נתוני דוגמה כדי שיהיה מה לראות ב-GUI
INSERT INTO projects (name) VALUES ('Project Alpha'), ('Project Beta');
INSERT INTO systems (project_id, name) VALUES (1, 'Main Control Unit'), (1, 'Navigation System');
INSERT INTO subassemblies (system_id, name) VALUES (1, 'Power Supply'), (1, 'CPU Board');ד