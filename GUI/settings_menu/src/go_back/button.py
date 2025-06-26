from GUI.settings_menu.src.go_back.action import go_back_action
from GUI.utils.buttons.RectangleButton import RectangleButton


def go_back_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=100, height=50, text='Back',
        batch=batch, group=group)
    
    button.on_press = lambda w: go_back_action(self_ptr, w)
    
    #self_ptr.push_handlers(button)

    return button