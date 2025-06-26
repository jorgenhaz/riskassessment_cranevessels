import pyglet
from pyglet.gui import PushButton
from GUI.simulation_menu.src.go_back.button import go_back_button
from GUI.simulation_menu.src.start_simulation.button import start_simulation_button
from GUI.simulation_menu.src.plot_simulation.button import plot_simulation_button
from GUI.simulation_menu.src.show_model.button import show_model_button
from GUI.simulation_menu.src.initial_values.button import set_params_button
from GUI.simulation_menu.src.set_wave_params.button import set_wave_params_button
from GUI.simulation_menu.src.set_sim_vals.button import set_sim_params_button
from GUI.simulation_menu.src.generate_wave_model.button import generate_wave_model_button

class SimulationMenu:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        self.background_group = pyglet.graphics.Group(order=-1)
        self.group_bg = pyglet.graphics.Group(order=0)
        self.group_fg = pyglet.graphics.Group(order=10)
        

        # _____Appending buttons here_____
        self.buttons.append(go_back_button(self.window, self.group_bg, 10, 10, self.batch))
        self.buttons.append(start_simulation_button(self.window, self.group_bg, 10, 180, self.batch))
        self.buttons.append(plot_simulation_button(self.window, self.group_bg, 10, 100, self.batch, self))
        self.buttons.append(show_model_button(self.window, self.group_bg, 10, 260, self.batch, self))
        self.buttons.append(set_params_button(self.window, self.group_bg, 900, 490, self.batch, self))
        self.buttons.append(set_wave_params_button(self.window, self.group_bg, 900, 570, self.batch, self))
        self.buttons.append(set_sim_params_button(self.window, self.group_bg, 900, 650, self.batch, self))
        self.buttons.append(generate_wave_model_button(self.window, self.group_bg, 900, 410, self.batch, self))
        # _____End appending buttons_____

        self.menu_label = pyglet.text.Label(
            "Simulation-tool",
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
        self.bg_image = pyglet.resource.image("images/boat3.png")
        self.bg_sprite = pyglet.sprite.Sprite(
            self.bg_image,
            x=0,
            y=0,
            batch=self.batch,
            group=self.background_group
        )
        self.bg_sprite.scale_x = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale_y = self.window.height / self.bg_sprite.height


        # Status message
        self.status = pyglet.text.Label(
            '', x=450, y=600,
            batch=self.batch, group=self.group_fg,
            color=(255, 0, 0, 255), font_size=20
        )

        
        

    def on_draw(self) -> None:
        self.window.clear()
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