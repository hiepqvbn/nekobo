# nekobo Project

**Nekobo** is an open-source robotics project that combines **hardware (FreeCAD, KiCad)** and **software (ROS2 + Python)** to create a small, cute, and hackable robot.  
The goal is to make a platform that is **easy to build, easy to program, and fun to extend**.

---

## ✨ Features (v0.1)

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

## 📂 Repository Structure

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

## 🚀 Getting Started

### 1. Clone repo

```bash
git clone https://github.com/hiepqvbn/nekobo.git
cd nekobo
```

### 2. Build container

```bash
docker build -t nekobo-dev ./container
```

### 3. Run hello-world ROS2 node

```bash
docker run -it --rm nekobo-dev
source /ros2_ws/install/setup.bash
ros2 run nekobo_pkg hello_node
```

You should see:

```bash
[INFO] [hello_node]: Hello Nekobo!
```

---

## Layout

![v0.1 Layout](./docs/layouts/nekobo-v0.1-system-layout.drawio.svg)

---

## 🛠 Hardware

- CAD: FreeCAD files

- PCB: KiCad files

- STL exports for 3D printing: STL folder

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
