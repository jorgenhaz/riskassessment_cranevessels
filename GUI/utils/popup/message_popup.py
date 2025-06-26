import pyglet
from pyglet.window import key
from pyglet import shapes

class MessagePopup(pyglet.event.EventDispatcher):

    def __init__(self, window, lines, title="Info"):
        self.window          = window
        self.prev_view       = window.current_view  
        window.current_view  = self                 

        self.batch = pyglet.graphics.Batch()
        self.bg = pyglet.shapes.Rectangle(80, 80, 840, 520,
                                          color=(50, 50, 50), batch=self.batch)

     
        self.title = pyglet.text.Label(
            title,
            x=100, y=560,
            font_size=16,
            color=(255, 255, 255, 255),
            batch=self.batch
        )


        self.labels = []                      

        for i, txt in enumerate(lines):
            lbl = pyglet.text.Label(
                txt,
                x=100, y=500 - i*25,
                color=(255, 255, 255, 255),
                batch=self.batch
            )
            self.labels.append(lbl)


    def on_draw(self):
        self.batch.draw()
        return True              

    def on_mouse_press(self, *_):
        self._close(); return True
    def on_key_press(self, symbol, _):
        if symbol == key.ESCAPE:
            self._close(); return True

    def _close(self):
        self.window.current_view = self.prev_view
        self.window.pop_handlers()
        self.window.invalid = True
