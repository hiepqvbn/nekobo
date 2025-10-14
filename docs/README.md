# Nekobo v0.1 — Development Notes

Welcome to the **official development notebook** for Nekobo v0.1.  
This folder contains all documentation, logs, and roadmap for the first version of the robot.

---

## 📦 Folder Structure

```
docs/
├── 0_preparation.md # Parts checklist, tools, and workspace setup
├── 1_device_test.md # Test logs for Arduino, Raspberry Pi, motors, and driver
├── 2_todo_list.md # Current tasks, checklist, and progress tracking
├── 3_roadmap.md # Project roadmap: v0.1 → v0.2 → v1.0
└── images/ # Photos, diagrams, wiring, and sketches
```

---

## 📝 How to Use This Documentation

### [1. Preparation](0_preparation.md)
- Confirm all hardware is present and functional.
- Organize your parts and tools into separate boxes.
- Log workspace setup and initial notes.

### [2. Device Test](1_device_test.md)
- Record results of individual hardware tests:
  - Raspberry Pi 4
  - Arduino Uno
  - DC motors
  - Motor driver
  - Controller input
  - Serial communication (Pi ↔ Arduino)
- Add screenshots or photos to `/images` for reference.

### [3. Todo List](2_todo_list.md)
- Track **all tasks** for v0.1.
- Use checkboxes `[ ]` for pending and `[x]` for completed tasks.
- Update this file every time a test or milestone is done.

### [4. Roadmap](3_roadmap.md)
- Outline **future development phases**:
  - v0.1: basic motion with controller
  - v0.2: mini middleware / simulation / ROS2 integration
  - v1.0+: AI robotics, multi-agent system

### [5. Images](images/)
- Store photos of:
  - Parts and tools
  - Wiring diagrams
  - Chassis prototypes
- Reference images in markdown like:
```markdown
![Parts Layout](images/parts_box.jpg)