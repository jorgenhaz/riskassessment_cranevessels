from GUI.utils.key_widgets.textinput import TextInput

def change_user_name_action(self, widget, group, batch, x, y):
    print("Write new username and press ENTER")
    
    text_input = TextInput(
        x=x,
        y=y,
        width=200,
        batch=batch,
        group=group,
        placeholder="New username"
    )
    
    self.push_handlers(text_input)

    def on_username_entered(new_username):
        print("New username: ", new_username)
        self.username = new_username
        self.user_label.text = "Welcome " + self.username
        self.remove_handlers(text_input)

    text_input.callback = on_username_entered
