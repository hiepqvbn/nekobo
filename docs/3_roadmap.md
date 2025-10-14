# Nekobo Project Roadmap

This document outlines the planned development phases for Nekobo, from the first MVP (v0.1) to more advanced AI and multi-agent versions.  
It is intended as a living roadmap — update it as the project evolves.

---

## 🌱 v0.1 — MVP: Basic Motion Control

**Goal:** Build a simple robot that can move using a controller.  
Focus on learning **hardware integration and control flow**.

### Key Features
- RC-style movement (forward/backward, turn left/right)
- Xbox One / Hori Fighting Stick controller input
- Raspberry Pi 4 + Arduino Uno for motor control
- Two DC motors with motor driver

### Milestones
1. Hardware preparation & testing
   - Test Raspberry Pi, Arduino, motors, motor driver, and controllers
2. Basic motion
   - Connect Arduino → motor driver → motors
   - Send commands from controller via Raspberry Pi
3. Temporary chassis
   - 2-wheel + caster base for testing motion
4. Documentation
   - Log tests and progress in `/docs` using GitHub repo

---

## 🚀 v0.2 — Motion + Local Network

**Goal:** Introduce networking and improve control.

### Key Features
- Raspberry Pi → PC/Laptop communication over Wi-Fi
- Centralized control using the PC as “brain” (optional for lightweight version)
- Prepare for later ROS2 integration
- Log telemetry from motors and controller

### Milestones
1. Setup local Wi-Fi network using old router
2. Implement communication protocol (e.g., serial, socket, or MQTT)
3. Record test logs and update documentation
4. Test temporary chassis with communication layer

---

## 🤖 v1.0 — Advanced Nekobo: AI & Multi-Agent Ready

**Goal:** Transform Nekobo into a modular AI robotics platform.

### Key Features
- Full chassis design (3D printed / parametric CAD)
- ROS2 integration for modular nodes
- AI perception (vision / SLAM)
- Multi-agent communication over Wi-Fi
- Safety mechanisms and local control fallback

### Milestones
1. Final mechanical design (chassis, mounting for electronics)
2. ROS2 node setup for motion and perception
3. Multi-agent coordination using router as network hub
4. Test AI control and autonomous motion
5. Document lessons learned for next iteration

---

## 📌 Notes

- Each version should **start from hardware validation**, then integrate software.  
- Use GitHub `/docs` as your official development notebook.  
- Keep your branches clean: one branch for notes, another for software code.  
- Always log experiments, failures, and ideas — this will help scale to multi-agent systems.

---

> This roadmap is **flexible** — adjust as you learn, test, and iterate.  
> The goal is **continuous learning and experimentation**, not rushing to a finished product.
