from GUI.simulation_menu.src.initial_values.action import set_params_init
from GUI.utils.buttons.RectangleButton import RectangleButton

def set_params_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=150, height=50, text='Initial values',
        batch=batch, group=group)
    
    button.on_press = lambda w: set_params_init(self_window_ptr, w)

    return button