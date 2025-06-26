from GUI.main_menu.src.about.action import about_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def about_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=100, height=50, text='About',
        batch=batch, group=group)
    
    button.on_press = lambda w: about_action(self_ptr, w)

    #self_ptr.push_handlers(button)

    return button