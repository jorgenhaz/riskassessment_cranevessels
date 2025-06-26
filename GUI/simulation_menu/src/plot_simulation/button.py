from GUI.simulation_menu.src.plot_simulation.action import plot_simulation_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def plot_simulation_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=170, height=50, text='Evaluate simulation',
        batch=batch, group=group)
    
    button.on_press = lambda w: plot_simulation_action(self_window_ptr, w, self_ptr)
    
    #self_ptr.push_handlers(button)

    return button