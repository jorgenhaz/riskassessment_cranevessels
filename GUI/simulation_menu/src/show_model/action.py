import subprocess, sys, os, threading
from pathlib import Path
import pyglet

def show_model_action(self, widget):
    print("show_model_action...")
    self.current_view.status.text = "Drawing model..."
    self.current_view.status.color = (255, 0, 0, 255)
    self.current_view.status.visible = True
    project_root = Path(__file__).resolve().parents[1] 
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    cmd = [
        sys.executable,
        "-m",
        "GUI.python_model.plotting_visual.draw_model_5",
    ]

    # Add to thread running in parallell 
    def worker():
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print("OK:\n", result.stdout)
        else:
            print("Error:\n", result.stderr)

        def update_status(dt):
            label = self.current_view.status
            self.current_view.status.color = (0, 255, 0, 255)
            label.text = "Done" if result.returncode == 0 else "Error"
            label.visible = True

        def hide_status(dt):
            self.current_view.status.visible = False

        pyglet.clock.schedule_once(update_status, 0)
        pyglet.clock.schedule_once(hide_status, 2)

    # Start thread - daemon=True quits when GUI closes
    threading.Thread(target=worker, daemon=True).start()