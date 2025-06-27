import pyglet
from pyglet import shapes

class RectangleButton(pyglet.event.EventDispatcher):
    def __init__(self, x, y, width, height, text, batch, group = None,
                 base_color = (50,100,200),
                 hover_color = (70, 120, 220),
                 press_color = (30, 80, 180),
                 text_color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.batch = batch
        self.group = group

        self.base_color = base_color
        self.hover_color = hover_color
        self.press_color = press_color
        self.text_color = text_color
        self.current_color = base_color

        self.background = shapes.Rectangle(x, y, width, height, color=self.current_color,
                                           batch = batch, group = group)
        
        self.label = pyglet.text.Label(
            text,
            font_name='Arial',
            font_size=14,
            x=x+width//2,
            y=y+height//2,
            anchor_x='center',
            anchor_y='center',
            color=text_color,
            batch=batch,
            group=group
        )

        self.on_press = None # This is set up externally

    """Is x,y within buttons area"""
    def hit_test(self,x,y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
    
    """Call from external mouse_press events, triggering on_press callback"""
    def click(self):
        if self.on_press:
            self.on_press(self)

    """Update background color"""
    def update_color(self, color):
        self.current_color = color
        self.background.color = color

    
    # Functions underneath are called by the window if the button is pushed to event-handlers
    

    """Hover color"""
    def on_mouse_motion(self, x, y, dx, dy):
        if self.hit_test(x,y):
            self.update_color(self.hover_color)
        else:
            self.update_color(self.base_color)

    """Press color and on_press-action"""
    def on_mouse_press(self, x, y, button, modifiers):
        if self.hit_test(x, y):
            self.update_color(self.press_color)
            if self.on_press:
                self.on_press(self)

    """Release color"""
    def on_mouse_release(self, x, y, button, modifiers):
        if self.hit_test(x, y):
            self.update_color(self.hover_color)
        else:
            self.update_color(self.base_color)