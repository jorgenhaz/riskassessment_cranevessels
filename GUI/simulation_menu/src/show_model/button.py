from GUI.simulation_menu.src.show_model.action import show_model_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def show_model_button(self_window_ptr, group, x,y, batch,self_ptr):

    button = RectangleButton(
        x, y, width=170, height=50, text='Show model',
        batch=batch, group=group)
    
    button.on_press = lambda w: show_model_action(self_window_ptr, w)
    
    #self_ptr.push_handlers(button)

    return button