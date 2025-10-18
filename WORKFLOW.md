# 🧠 Nekobo Development Workflow

This document describes the lightweight but scalable workflow for developing Nekobo.  
The goal is to stay simple for solo work while remaining clean, consistent, and ready for collaboration.

---

## ⚙️ 1. Branch Structure

| Branch     | Purpose                                                                    |
| ---------- | -------------------------------------------------------------------------- |
| `main`     | Stable and tested version. Each release (v0.1, v0.2, etc.) is merged here. |
| `v*-notes` | For notes, sketches, wiring ideas, docs, and brainstorming.                |
| `v*-dev`   | Main development branch for writing new code.                              |
| `v*-test`  | Testing and tuning hardware; bridge between dev and main.                  |

**Example:**

    main
    ├── v0.1-notes
    ├── v0.1-dev
    └── v0.1-test

---

## 🧱 2. Typical Flow for a Version (e.g. v0.1)

1. Create notes branch for design ideas

   ```bash
   git checkout -b v0.1-notes
   ```

2. Create development branch

   ```bash
   git checkout -b v0.1-dev
   ```

3. Code, commit, and push progress regularly.
4. Create testing branch from dev when ready to test hardware.

   ```
   git checkout -b v0.1-test
   ```

5. Test, fix, and confirm stable operation.
6. Merge back into main and tag release:

   ```bash
   git checkout main
   git merge v0.1-test
   git tag v0.1
   git push origin main --tags
   ```

---

## 💬 3. Commit Message Style

Use clear, consistent messages:

```vbnet
feat: add motor control class
fix: correct PWM direction pin
docs: update wiring diagram
refactor: cleanup serial interface
test: add debug print for joystick
```

| Type        | Meaning                             |
| ----------- | ----------------------------------- |
| `feat:`     | Add new feature                     |
| `fix:`      | Fix a bug                           |
| `docs:`     | Update documentation                |
| `refactor:` | Code cleanup without changing logic |
| `test:`     | Add or modify test/debug functions  |

---

## 🔄 4. Code Deployment

### Raspberry Pi 4

Clone once, then pull updates:

```bash
git clone -b v0.1-test https://github.com/hiepqvbn/nekobo.git
cd nekobo
git pull
```

### Arduino

Keep `.ino` files inside `firmware/arduino_motor/`.

Upload using `Arduino IDE` or later automate with `arduino-cli`.

---

## 🚀 5. Release Notes

- After each version is complete:
- Update docs/3_roadmap.md
- Add a short summary of what was achieved
- Tag the release:
  ```bash
  git tag v0.1
  git push origin main --tags
  ```

---

## 🧩 6. Future Scaling

When you collaborate later:

- Each person works on their own feature branch: `feature/motor_refactor`, `feature/sensor_add`
- Use Pull Requests to merge into `dev`
- Keep `main` always deployable

---

Keep it clean. Keep it simple. Build fast and smart.
