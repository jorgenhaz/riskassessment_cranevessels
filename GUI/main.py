import pyglet
from GUI.main_menu.menu import MainMenu
from GUI.settings_menu.menu import SettingsMenu
from GUI.simulation_menu.menu import SimulationMenu

class AppWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1080, height=720, caption="Risk assessment - demo", resizable=True)
        self.set_location(0, 0)
        self.set_mouse_visible(True)

        self.group_bg = pyglet.graphics.Group(order=0)
        self.group_fg = pyglet.graphics.Group(order=1)
        self.batch = pyglet.graphics.Batch()

        self.views = {
            "main": MainMenu(self),
            "settings": SettingsMenu(self),
            "simulation": SimulationMenu(self),
        }

        self.current_view = self.views["main"]

    def change_view(self, name):
        if name in self.views:
            self.current_view = self.views[name]


    def on_draw(self):

        self.clear()
        self.current_view.on_draw()
        

    def on_mouse_press(self, x, y, button, modifiers):

        if hasattr(self.current_view, "on_mouse_press"):
            self.current_view.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if hasattr(self.current_view, "on_mouse_motion"):
            self.current_view.on_mouse_motion(x,y,dx,dy)
    
    def on_mouse_release(self, x, y, button, modifiers):
        if hasattr(self.current_view, "on_mouse_release"):
            self.current_view.on_mouse_release(x, y, button, modifiers)

if __name__ == "__main__":
    window = AppWindow()
    pyglet.app.run()
