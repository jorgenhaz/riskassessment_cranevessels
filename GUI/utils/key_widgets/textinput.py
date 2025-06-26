import pyglet
from pyglet.window import key
from pyglet import shapes

class TextInput:
    def __init__(self, x, y, width, batch, group=None, placeholder=""):
        self.x=x
        self.y=y
        self.width=width
        self.batch=batch
        self.group=group
        self.placeholder=placeholder
        self.text=""

        self.label=pyglet.text.Label(self.placeholder if self.text=="" else self.text,
                                     font_name='Arial',
                                     font_size=14,
                                     x=x,
                                     y=y,
                                     anchor_x='left',
                                     anchor_y='center',
                                     color=(0,0,0,255),
                                     batch=batch,
                                     group=group)
        
        # Making a square around text-input to encapsulate
        self.labelRectangle = shapes.Rectangle(x=x,y=y-25,width=width, height=50,
                                               color=(100,100,100,255), batch=batch,
                                               group=group)
        self.labelRectangle.opacity = 30

        self.active = True              # Input field is active
        self.callback = None            # Function called when user press ENTER

    def on_text(self, text):
        if self.active:
            self.text += text
            self.label.text = self.text

    def dispose(self):
        self.label.delete()
        self.labelRectangle.delete()

    def on_key_press(self, symbol, modifiers):
        if self.active:
            if symbol == key.BACKSPACE:
                self.text = self.text[:-1]
                self.label.text = self.text if self.text != "" else self.placeholder
            elif symbol == key.ENTER:
                self.active = False
                if self.callback:
                    self.callback(self.text)
                    self.dispose()