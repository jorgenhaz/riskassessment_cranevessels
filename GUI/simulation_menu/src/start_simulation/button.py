from GUI.simulation_menu.src.start_simulation.action import start_simulation_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def start_simulation_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=170, height=50, text='Start simulation',
        batch=batch, group=group)
    
    button.on_press = lambda w: start_simulation_action(self_ptr, w)
    
    #self_ptr.push_handlers(button)

    return button