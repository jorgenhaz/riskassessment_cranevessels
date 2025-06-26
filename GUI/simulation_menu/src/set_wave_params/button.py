from GUI.simulation_menu.src.set_wave_params.action import set_wave_params
from GUI.utils.buttons.RectangleButton import RectangleButton

def set_wave_params_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=150, height=50, text='Wave params.',
        batch=batch, group=group)
    
    button.on_press = lambda w: set_wave_params(self_window_ptr, w)

    return button