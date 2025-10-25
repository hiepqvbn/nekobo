import pygame

pygame.init()
pygame.joystick.init()

def init_pygame():
    """Initialize pygame modules required for joysticks.

    Safe to call multiple times.
    """
    if not pygame.get_init():
        pygame.init()
    pygame.joystick.init()


def init_joystick(index: int = 0):
    """Return an initialized pygame joystick instance.

    Raises IndexError if no joystick found at index.
    """
    init_pygame()
    if pygame.joystick.get_count() <= index:
        raise IndexError(f"No joystick available at index {index}")
    js = pygame.joystick.Joystick(index)
    js.init()
    return js


def get_joystick_info(js):
    """Return basic info about the joystick as a dictionary."""
    return {
        "name": js.get_name(),
        "num_axes": js.get_numaxes(),
        "axes": [js.get_axis(i) for i in range(js.get_numaxes())],
        "num_hats": js.get_numhats(),
        "hats": [js.get_hat(i) for i in range(js.get_numhats())],
        "num_buttons": js.get_numbuttons(),
        "buttons": [js.get_button(i) for i in range(js.get_numbuttons())],
    }


def quit_pygame():
    """Cleanly quit pygame when finished."""
    try:
        pygame.joystick.quit()
    except Exception:
        pass
    try:
        pygame.quit()
    except Exception:
        pass
