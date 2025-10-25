from typing import Optional, Dict, Any
from .base import BaseController
from .controller_helper import init_joystick, quit_pygame
import pygame


class HoriMiniFightstickController(BaseController):
    def __init__(self, name: str = "hori_fightstick", joystick_index: int = 0) -> None:
        """Controller adapter for a Hori Mini Fightstick (USB joystick).

        Reads pygame joystick hats/axes and translates to high-level MOVE/STOP
        commands.
        """
        super().__init__(name=name)
        self.joystick_index = joystick_index
        self.js = None

    def start(self) -> None:
        try:
            self.js = init_joystick(self.joystick_index)
        except Exception:
            self.js = None
        super().start()

    def stop(self) -> None:
        try:
            if self.js:
                self.js.quit()
        except Exception:
            pass
        quit_pygame()
        super().stop()

    def read_input(self) -> Optional[Dict[str, Any]]:
        if not self.js:
            return None
        try:
            # ensure pygame event queue is processed
            pygame.event.pump()
            # prefer hats if available
            if self.js.get_numhats() > 0:
                hat = self.js.get_hat(0)
                x, y = hat[0], hat[1]
            else:
                # fallback to axes (typical fightstick maps)
                x = int(self.js.get_axis(0) * 1)
                y = int(-self.js.get_axis(1) * 1)
            if x == 0 and y == 0:
                return {"type": "STOP"}
            # simple mapping: y controls forward/back, x for left/right
            speed = int(200 * y)
            left = speed
            right = speed
            if x != 0:
                left = left - 100 * x
                right = right + 100 * x
            return {"type": "MOVE", "speed_left": int(left), "speed_right": int(right)}
        except Exception:
            return None


if __name__ == '__main__':
    # When executed as a script, load the base test harness from the same
    # package and run the visual test using this controller instance.
    import importlib.util
    import os
    import sys

    base_path = os.path.join(os.path.dirname(__file__), 'base.py')
    spec = importlib.util.spec_from_file_location('controller_base', base_path)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)

    c = HoriMiniFightstickController()
    base.run_visual_test(c)
    
# from typing import Optional, Dict, Any
# from .base import BaseController
# from .controller_helper import init_joystick, quit_pygame
# import pygame


# class HoriMiniFightstickController(BaseController):
#     def __init__(self, name: str = "hori_fightstick", joystick_index: int = 0) -> None:
#         """Controller adapter for a Hori Mini Fightstick (USB joystick).

#         Reads pygame joystick hats/axes and translates to high-level MOVE/STOP
#         commands.
#         """
#         super().__init__(name=name)
#         self.joystick_index = joystick_index
#         self.js = None

#     def start(self) -> None:
#         try:
#             self.js = init_joystick(self.joystick_index)
#         except Exception:
#             self.js = None
#         super().start()

#     def stop(self) -> None:
#         try:
#             if self.js:
#                 self.js.quit()
#         except Exception:
#             pass
#         quit_pygame()
#         super().stop()

#     def read_input(self) -> Optional[Dict[str, Any]]:
#         if not self.js:
#             return None


# if __name__ == '__main__':
#     # When executed as a script, load the base test harness from the same
#     # package and run the visual test using this controller instance.
#     import importlib.util
#     import os
#     import sys

#     base_path = os.path.join(os.path.dirname(__file__), 'base.py')
#     spec = importlib.util.spec_from_file_location('controller_base', base_path)
#     base = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(base)

#     c = HoriMiniFightstickController()
#     base.run_visual_test(c)
#         try:
#             # ensure pygame event queue is processed
#             pygame.event.pump()
#             # prefer hats if available
#             if self.js.get_numhats() > 0:
#                 hat = self.js.get_hat(0)
#                 x, y = hat[0], hat[1]
#             else:
#                 # fallback to axes (typical fightstick maps)
#                 x = int(self.js.get_axis(0) * 1)
#                 y = int(-self.js.get_axis(1) * 1)
#             if x == 0 and y == 0:
#                 return {"type": "STOP"}
#             # simple mapping: y controls forward/back, x for left/right
#             speed = int(200 * y)
#             left = speed
#             right = speed
#             if x != 0:
#                 left = left - 100 * x
#                 right = right + 100 * x
#             return {"type": "MOVE", "speed_left": int(left), "speed_right": int(right)}
#         except Exception:
#             return None
