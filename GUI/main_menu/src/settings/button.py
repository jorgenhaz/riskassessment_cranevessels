from GUI.main_menu.src.settings.action import settings_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def settings_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=100, height=50, text='Settings',
        batch=batch, group=group)
    
    button.on_press = lambda w: settings_action(self_ptr, w)
    
    #self_ptr.push_handlers(button)

    return button