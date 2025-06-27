from GUI.settings_menu.src.change_user_name.action import change_user_name_action
from GUI.utils.buttons.RectangleButton import RectangleButton

def change_user_name_button(self_ptr, group, x,y, batch):

    button = RectangleButton(
        x, y, width=180, height=50, text='Change user-name',
        batch=batch, group=group)
    
    button.on_press = lambda w: change_user_name_action(self_ptr, w, group=group, batch=batch, x=(x+200), y=(y+25))
    
    return button