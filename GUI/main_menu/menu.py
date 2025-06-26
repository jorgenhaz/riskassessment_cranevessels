import pyglet
from pyglet.gui import PushButton
from GUI.main_menu.src.settings.button import settings_button
from GUI.main_menu.src.about.button import about_button
from GUI.main_menu.src.simulation.button import simulation_button

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        self.background_group = pyglet.graphics.Group(order=-1)
        self.group_bg = pyglet.graphics.Group(order=0)
        self.group_fg = pyglet.graphics.Group(order=1)

        self.window.username = "USER"

        # _____Appending buttons here_____

        self.buttons.append(settings_button(self.window, self.group_bg, 10, 100, self.batch))
        self.buttons.append(about_button(self.window, self.group_bg, 10, 180, self.batch))
        self.buttons.append(simulation_button(self.window, self.group_bg, 10, 240, self.batch))

        # _____End appending buttons_____

        self.menu_label = pyglet.text.Label(
            "Risk assessment - demo",
            font_name='Courier New',
            font_size=16,
            x=5,
            y=self.window.height - 25,
            anchor_x="left",
            anchor_y="center",
            color=(0,0,0,255),
            batch=self.batch,
            group=self.group_bg
        )

        self.window.user_label = pyglet.text.Label(
            text= "Welcome " + self.window.username,
            font_name='Courier New',
            font_size=16,
            x=5,
            y=self.window.height - 50,
            anchor_x="left",
            anchor_y="center",
            color=(0,0,0,255),
            batch=self.batch,
            group=self.group_bg
        )

        self.bg_image = pyglet.resource.image("images/boat.png")
        self.bg_sprite = pyglet.sprite.Sprite(
            self.bg_image,
            x=0,
            y=0,
            batch=self.batch,
            group=self.background_group
        )
        self.bg_sprite.scale_x = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale_y = self.window.height / self.bg_sprite.height

    def on_draw(self) -> None:
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            if hasattr(btn, "on_mouse_press"):
                btn.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons:
            if hasattr(btn, "on_mouse_motion"):
                btn.on_mouse_motion(x, y, dx, dy)
                
    def on_mouse_release(self, x, y, button, modifiers):
        for btn in self.buttons:
            if hasattr(btn, "on_mouse_release"):
                btn.on_mouse_release(x, y, button, modifiers)

