#!/usr/bin/env python3
"""Controller base classes and manager.

This module defines a high-level BaseController interface that each
hardware-specific controller should implement. The ControllerManager
composes one or more controllers and exposes a simple `read_input()`
method for the application to poll.

Design:
- BaseController: abstract base class for hardware controllers. Implements
  lifecycle hooks and requires `read_input()` to return a high-level dict
  consumable by the Bridge/application.
- ControllerManager: accept multiple BaseController instances and return
  the highest-priority non-empty input from them.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import time


class BaseController(ABC):
    """Abstract controller interface.

    Implementations should be responsible for low-level hardware access
    (pygame joystick, smbus nunchuk, etc.) and translate raw input into
    a small set of high-level commands the application understands, for
    example:

      {"type": "MOVE", "speed_left": 100, "speed_right": -100}
      {"type": "STOP"}
      {"type": "SET_LED", "r": 255, "g": 0, "b": 128}

    Methods should be non-blocking where possible and return None when
    no meaningful input is available.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.started = False

    def start(self) -> None:
        """Start or initialize hardware resources. Optional to override."""
        self.started = True

    def stop(self) -> None:
        """Release hardware resources. Optional to override."""
        self.started = False

    @abstractmethod
    def read_input(self) -> Optional[Dict[str, Any]]:
        """Read and return a high-level input dict or None.

        This method should be fast and non-blocking.
        """


class ControllerManager:
    """Manage multiple BaseController instances and provide a unified view.

    The manager polls controllers in order and returns the first non-empty
    input. This allows prioritizing e.g. a USB fightstick over a nunchuk.
    """

    def __init__(self, controllers: Optional[List[BaseController]] = None) -> None:
        self.controllers: List[BaseController] = controllers or []

    def add(self, controller: BaseController) -> None:
        self.controllers.append(controller)
        controller.start()

    def remove(self, controller: BaseController) -> None:
        try:
            self.controllers.remove(controller)
        except ValueError:
            pass
        controller.stop()

    def read_input(self) -> Optional[Dict[str, Any]]:
        """Poll controllers and return the first non-empty high-level input.

        Returns None if no controller reports input (i.e., idle).
        """
        for c in self.controllers:
            try:
                data = c.read_input()
            except Exception:
                data = None
            if data:
                return data
        return None

    def shutdown(self) -> None:
        for c in list(self.controllers):
            try:
                c.stop()
            except Exception:
                pass


def run_visual_test(controller: Optional[BaseController] = None, width: int = 640, height: int = 480) -> None:
    """Run a small pygame visual test window to exercise a controller.

    If `controller` is None, a simple keyboard controller is used. The
    window shows a rectangle that can move and rotate according to the
    high-level MOVE/STOP commands produced by controllers.
    """
    try:
        import pygame
    except Exception as exc:  # pragma: no cover - depends on runtime
        raise RuntimeError("pygame is required to run the visual test") from exc

    # Local keyboard-backed controller implementation
    class KeyboardController(BaseController):
        def __init__(self) -> None:
            super().__init__(name="keyboard")

        def start(self) -> None:
            try:
                from .controller_helper import init_pygame
                init_pygame()
            except Exception:
                pass
            super().start()

        def stop(self) -> None:
            try:
                from .controller_helper import quit_pygame
                quit_pygame()
            except Exception:
                pass
            super().stop()

        def read_input(self):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            # arrow keys control forward/back and turning
            f = 0
            t = 0
            if keys[pygame.K_UP]:
                f = 1
            if keys[pygame.K_DOWN]:
                f = -1
            if keys[pygame.K_RIGHT]:
                t = -1
            if keys[pygame.K_LEFT]:
                t = 1
            if f == 0 and t == 0:
                return {"type": "STOP"}
            # map to speeds similar to hardware controllers
            speed = int(f * 200)
            turn = int(t * 100)
            left = speed - turn
            right = speed + turn
            return {"type": "MOVE", "speed_left": left, "speed_right": right}

    # choose controller
    ctrl = controller if controller is not None else KeyboardController()
    try:
        ctrl.start()
    except Exception:
        pass
    import math
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    rect = pygame.Surface((80, 48), pygame.SRCALPHA)
    rect.fill((200, 100, 50))
    rect_center = [width // 2, height // 2]
    angle = 0.0

    font = None
    try:
        font = pygame.font.Font(None, 20)
    except Exception:
        font = None

    running = True
    try:
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    running = False

            data = None
            try:
                data = ctrl.read_input()
            except Exception:
                data = None

            # default motion
            vx = 0.0
            vy = 0.0
            ang_speed = 0.0
            forward = 0.0
            turn = 0.0
            if data and data.get("type") == "MOVE":
                left = float(data.get("speed_left", 0))
                right = float(data.get("speed_right", 0))
                forward = (left + right) / 2.0
                turn = (right - left) / 2.0
                # scale for pixels per second
                speed_px = forward * 0.5
                ang_speed = turn * 0.3
                # compute movement in heading direction
                
                rad = math.radians(angle)
                vx = math.cos(rad) * speed_px
                vy = -math.sin(rad) * speed_px

            dt = clock.tick(60) / 1000.0
            rect_center[0] += vx * dt
            rect_center[1] += vy * dt
            angle += ang_speed * dt

            screen.fill((30, 30, 30))
            rotated = pygame.transform.rotate(rect, angle)
            r = rotated.get_rect(center=tuple(rect_center))
            screen.blit(rotated, r)

            # HUD
            if font:
                lines = ["Controller: %s" % ctrl.name, "ESC to quit", f'angle: {angle:.1f}',
                         f'forward:{forward:.1f} turn:{turn:.1f}']
                y = 8
                for ln in lines:
                    surf = font.render(ln, True, (220, 220, 220))
                    screen.blit(surf, (8, y))
                    y += 18

            pygame.display.flip()

    finally:
        try:
            ctrl.stop()
        except Exception:
            pass
        try:
            from .controller_helper import quit_pygame
            quit_pygame()
        except Exception:
            try:
                pygame.quit()
            except Exception:
                pass


if __name__ == "__main__":
    # When run directly, open the visual test with keyboard controls.
    run_visual_test(None)

