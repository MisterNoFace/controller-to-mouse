import pygame,mouse,asyncio,desktop_notifier
import webbrowser,os,shutil
pygame.init()
pygame.joystick.init()

autoload_folder='C:/Users/'+os.getlogin()+'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'

notifier = desktop_notifier.DesktopNotifier()
async def on_device_connected():
    if os.path.exists(autoload_folder+'/'+os.path.basename(__file__)):
        await notifier.send(
            title="Device Connected Successfully",
            message='Your device is connected and ready to use. Press the HOME BUTTON to enable/disable the controller.',
            buttons=[
                desktop_notifier.Button(
                    title="Disable Autoload on Startup",
                    on_pressed=lambda: os.remove(autoload_folder+'/'+os.path.basename(__file__))
                ),
                ]
            )
    else:
        await notifier.send(
            title="Device Connected Successfully",
            message='Your device is connected and ready to use. Press the HOME BUTTON to enable/disable the controller.',
            buttons=[
                desktop_notifier.Button(
                    title="Enable Autoload on Startup",
                    on_pressed=lambda: shutil.copy(__file__,autoload_folder+'/'+os.path.basename(__file__))
                ),
                ]
            )
async def on_device_disconnected():
    await notifier.send(
        title="Device Disconnected",
        message='You disconnected a device. Automatically disabled the controller.',
        buttons=[
            desktop_notifier.Button(
                title="Exit Application",
                on_pressed=lambda: pygame.quit()
            ),
            desktop_notifier.Button(
                title="Read Documentation",
                on_pressed=lambda: webbrowser.open('https://github.com/MisterNoFace/controller-to-mouse')
            ),
            ]
        )

clock = pygame.time.Clock()
mouse_speed=8
joystick = None
is_active = False
axis=[0,0]

def sign(x):
    if x > 0.3:
        return 1
    elif x < -0.3:
        return -1
    else:
        return 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.JOYDEVICEADDED:
            joystick=pygame.joystick.Joystick(0)
            is_active=True
            asyncio.run(on_device_connected())
        if event.type == pygame.JOYDEVICEREMOVED:
            joystick=None
            is_active = False
            asyncio.run(on_device_disconnected())
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 10:
                is_active = not is_active

        if is_active:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    mouse.press(button='left')
                if event.button == 1:
                    mouse.right_click()
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    mouse.release(button='left')
        
    if is_active:
        axis[0] = sign(joystick.get_axis(0))
        axis[1] = sign(joystick.get_axis(1))
        if not joystick.get_button(2):
            axis[0] *= mouse_speed
            axis[1] *= mouse_speed
        mouse.move(mouse.get_position()[0] + axis[0], mouse.get_position()[1] + axis[1])
        if sign(joystick.get_axis(3))!=0:
            mouse.wheel(-sign(joystick.get_axis(3)))
            clock.tick(30*abs(joystick.get_axis(3)))
        else:
            clock.tick(120)