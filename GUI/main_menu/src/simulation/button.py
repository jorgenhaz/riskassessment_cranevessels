from GUI.main_menu.src.simulation.action import simulation_menu_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def simulation_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=100, height=50, text='Simulation',
        batch=batch, group=group)
    
    button.on_press = lambda w: simulation_menu_action(self_ptr, w)

    return button