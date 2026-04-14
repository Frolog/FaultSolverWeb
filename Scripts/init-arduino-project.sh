#!/bin/bash

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./init-arduino-project.sh ProjectName"
  exit 1
fi

# Create project folders
mkdir -p "$PROJECT_NAME"/{docs,lib}

# Arduino sketch (must be in root folder for Arduino IDE)
cat <<EOF > "$PROJECT_NAME/$PROJECT_NAME.ino"
void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println("Project: $PROJECT_NAME");
  delay(2000);
}
EOF

# Copy placeholder schematic
cp "/c/Users/dev30/PersonalGitRepos/Scripts/placeholder.png" "$PROJECT_NAME/docs/schematic.png" 2>/dev/null

# README template
cat <<EOF > "$PROJECT_NAME/README.md"
# $PROJECT_NAME

Arduino / ESP32 project.

## Features

- ESP32 based project
- MQTT communication
- Web server

## Hardware

- ESP32
- Sensor module
- WiFi network

## 🔌 Wiring

| Sensor Pin | Arduino Pin |
|------------|-------------|
| VCC        | 5V          |
| GND        | GND         |
| DATA       | D2          |

## 📷 Schematic

![Schematic](docs/schematic.png)

*(replace with your schematic if needed)*

## Project Structure

\`\`\`
$PROJECT_NAME
│
├── $PROJECT_NAME.ino
├── docs
│   └── schematic.png
├── lib
├── README.md
└── .gitignore
\`\`\`

## Upload

1. Open Arduino IDE
2. Select board ESP32 / Arduino UNO
3. Select COM Port
4. Upload sketch

EOF

# gitignore
cat <<EOF > "$PROJECT_NAME/.gitignore"
# Arduino build files
*.bin
*.elf
*.hex
*.o
*.a

# temp files
*.log
*.tmp

# OS
.DS_Store
Thumbs.db
EOF

# Initialize Git repository
cd "$PROJECT_NAME"
git init

echo "✅ Project $PROJECT_NAME created with README and placeholder schematic!"