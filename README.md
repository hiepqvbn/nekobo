# `nekobo` Project

`nekobo` is an open-source, modular robot platform inspired by a cat 🐱 — small, cute, and hackable.
It combines **hardware (FreeCAD, KiCad)** and **software (ROS2 + Python)** to create a robot that’s:
🧩 **Modular**, 🛠 **DIY-friendly**, and 🎓 **Educational**.

---

## 🌱 Project Vision

- Make robotics accessible and joyful for makers, students, and hobbyists
- Use simple mechanical design
- Keep the system modular
- Maintain open documentation so anyone can replicate and learn

---

## Current Version: v0.1b

Goal: Make the first replicable version of Nekobo — anyone can follow the guide and get the same result.

- Use common materials (wood or acrylic)
- Keep design fully open and DIY-friendly
- Verify control flow: Controller → Raspberry Pi 4 → Arduino → 2 DC motors

### ✨ Features

- Hardware:
  - First FreeCAD model (`.fcstd`) + STL export for 3D printing
  - Early draft of KiCad schematic
  - Basic Bill of Materials (BOM)
- Software:
  - Minimal ROS2 package (`nekobo_pkg`)
  - Hello-world ROS2 node to test setup
- Container:
  - Dockerfile for reproducible dev environment (ROS2 + Python3)

---

### Layout

## ![v0.1 Layout](./docs/layouts/nekobo-v0.1-system-layout.drawio.svg)

### 📂 Repository Structure

```
nekobo/
├── hardware/ # CAD + PCB
│ ├── freecad/
│ ├── kicad/
│ └── docs/ # BOM, exports (STL, PDF)
├── software/ # ROS2 workspace + scripts
├── container/ # Dockerfile + setup
├── docs/ # Guides, roadmap
├── LICENSE # See "Licenses" section
└── README.md
```

---

### 🚀 Getting Started

#### 1. Clone repo

```bash
git clone https://github.com/hiepqvbn/nekobo.git
cd nekobo
```

---

### 🛠 Hardware

- CAD: FreeCAD files

- BOM (Bill of Materials)

---

## 📅 Roadmap

See docs/roadmap.md for details.
Planned features include:

- Ball-following demo

- Voice command + sound feedback

- Mobile platform expansion

- Modular add-ons (sensors, arms)

---

## 🤝 Contributing

We welcome contributions!
Check CONTRIBUTING.md for guidelines on code style, CAD conventions, and PR process.

---

## ⚖️ Licenses

Hardware (FreeCAD, KiCad) → CERN-OHL-W v2

Software (ROS2, Python) → Apache 2.0

---

## 📸 Media

(Add an image or GIF of Nekobo here — even a FreeCAD screenshot works!)

---

## 💬 Community

Discussions: GitHub Discussions (planned)

Issues: Use GitHub Issues
for bugs and feature requests

---

Made with ❤️ by Hip and contributors.
