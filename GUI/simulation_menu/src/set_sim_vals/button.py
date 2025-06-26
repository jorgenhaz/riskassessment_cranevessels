from GUI.simulation_menu.src.set_sim_vals.action import set_sim_params
from GUI.utils.buttons.RectangleButton import RectangleButton

def set_sim_params_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=150, height=50, text='Sim. params.',
        batch=batch, group=group)
    
    button.on_press = lambda w: set_sim_params(self_window_ptr, w)

    return button