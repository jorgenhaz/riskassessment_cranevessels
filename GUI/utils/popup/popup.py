import pyglet
from pyglet.window import key
from ruamel.yaml.scalarstring import ScalarString 
from pyglet import shapes

class ParamPopup(pyglet.event.EventDispatcher):
    def __init__(self, window, title, params: dict, on_ok):

        self.window = window
        self.params = params
        self.on_ok  = on_ok
        self._in_edit = False

        self.batch = pyglet.graphics.Batch()
        self.batch_bg = pyglet.graphics.Batch()
        self.bg = pyglet.shapes.Rectangle(80, 80, 840, 520,
                                          color=(50, 50, 50), batch=self.batch)
        
        # Image related
        self.bg_image = pyglet.resource.image("images/boat3.png")
        self.bg_sprite = pyglet.sprite.Sprite(
            self.bg_image,
            x=0,
            y=0,
            batch=self.batch
        )
        self.bg_sprite.scale_x = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale_y = self.window.height / self.bg_sprite.height
        self.bg_sprite.opacity = 0
        self.title = pyglet.text.Label(
            title,
            x=100, y=560,
            font_size=16,
            color=(255, 255, 255, 255),
            batch=self.batch
        )

        self.fields = []
        max_rows = 15           
        start_y  = 520

        for i, (k, v) in enumerate(params.items()):
            row = i % max_rows             
            col = i // max_rows             
            x_label = 100 + col * 300       
            y = start_y - 30 * row

            self.fields.append({
                "key": k,
                "label": pyglet.text.Label(f"{k}:",
                                        x=x_label, y=y, batch=self.batch),
                "edit":  pyglet.text.Label(str(v),
                                        x=x_label + 160, y=y, batch=self.batch),
            })
        self.current_idx = 0
        self._highlight_current()

    def on_draw(self):
        self.batch.draw()
        return True   

    def _move(self, delta):
        self._unhighlight_current()
        self.current_idx = (self.current_idx + delta) % len(self.fields)
        self._highlight_current()

    def _highlight_current(self):
        self.fields[self.current_idx]["label"].color = (255, 200, 0, 255)

    def _unhighlight_current(self):
        self.fields[self.current_idx]["label"].color = (255, 255, 255, 255)

    def _edit_current(self):
        """Går inn i edit-modus for valgt felt."""
        field = self.fields[self.current_idx]
        self._in_edit = True

        def on_text(text):
            field["edit"].text += text

        def on_text_motion(motion):
            if motion == key.MOTION_BACKSPACE:
                field["edit"].text = field["edit"].text[:-1]

        def on_key_press(sym, _mod):
            if sym == key.ENTER:
                txt = field["edit"].text.strip()

                if txt == '':
                    new_val = ''
                else:
                    try:
                        new_val = int(txt)
                    except ValueError:
                        try:
                            new_val = float(txt)
                        except ValueError:
                            new_val = txt
                node = self.params[field["key"]]
                if hasattr(node, "yaml_set_scalar_style") and not isinstance(new_val, ScalarString):
                    node.yaml_set_scalar_style(None)

                self.params[field["key"]] = new_val

                self.window.pop_handlers()
                self._in_edit = False
                return True
            return False  

        self.window.push_handlers(
            on_text=on_text,
            on_text_motion=on_text_motion,
            on_key_press=on_key_press,
        )

    def on_key_press(self, symbol, modifiers):

        if symbol == key.UP:
            self._move(-1)
            return True
        if symbol == key.DOWN:
            self._move(1)
            return True

        if symbol == key.SPACE and not getattr(self, "_in_edit", False):
            self._edit_current()
            return True

        if symbol == key.ENTER:
            if callable(self.on_ok):
                self.on_ok()
            return True
        if symbol == key.ESCAPE:
            self.window.pop_handlers()
            self.window.current_popup = None
            self.window.invalid = True
            return True


        return False

    def _cancel(self):
        self.on_ok()        