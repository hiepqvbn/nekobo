import pygame

pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()

print("Controller:", js.get_name())
print("Number of axes:", js.get_numaxes())
for i in range(js.get_numaxes()):
    print(f"Axis {i}: {js.get_axis(i)}")

print("Number of buttons:", js.get_numbuttons())
for i in range(js.get_numbuttons()):
    print(f"Button {i}: {js.get_button(i)}")

pygame.quit()
