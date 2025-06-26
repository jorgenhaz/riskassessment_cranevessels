from GUI.simulation_menu.src.generate_wave_model.action import generate_wave_model_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def generate_wave_model_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=150, height=50, text='Generate waves',
        batch=batch, group=group)
    
    button.on_press = lambda w: generate_wave_model_action(self_window_ptr, w)

    return button