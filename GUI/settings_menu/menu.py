import pyglet
from pyglet.gui import PushButton
from GUI.settings_menu.src.change_user_name.button import change_user_name_button
from GUI.settings_menu.src.go_back.button import go_back_button

class SettingsMenu:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        self.background_group = pyglet.graphics.Group(order=-1)
        self.group_bg = pyglet.graphics.Group(order=0)
        self.group_fg = pyglet.graphics.Group(order=1)

        # _____Appending buttons here_____

        self.buttons.append(change_user_name_button(self.window, self.group_bg, 
                                                    10, 500, self.batch))
        self.buttons.append(go_back_button(self.window, self.group_bg, 10, 10, self.batch))

        # _____End appending buttons_____
        self.menu_label = pyglet.text.Label(
            "Settings",
            font_size=24,
            font_name='Courier New',
            x=5,
            y=self.window.height - 25,
            anchor_x="left",
            anchor_y="center",
            color=(0,0,0,255),
            batch=self.batch,
            group=self.group_bg
        )
        
        self.bg_image = pyglet.resource.image("images/boat2.png")
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