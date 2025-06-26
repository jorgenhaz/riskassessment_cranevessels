import subprocess, sys, os, threading, shutil
from pathlib import Path
import pyglet

def generate_wave_model_action (self, widget):
        # Messsages
        print("Generate new wave model and compiling cpp-directory...")
        self.current_view.status.text = "Generating wave model..."
        self.current_view.status.color = (255, 0, 0, 255)
        self.current_view.status.visible = True

        # Root path
        project_root = Path.cwd()

        # Command
        cmd = [
            sys.executable,
            "-m",
            "GUI.python_model.waves.wave_potential",
        ]

        # Add to thread running in parallell 
        def worker():
            result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)

            if result.returncode == 0:
                print("OK:\n", result.stdout)
                cpp_dir = project_root / "cpp_gui"

                subprocess.run(
                     ["cmake", "-B", "build"],
                     cwd=cpp_dir,
                     check=True
                )
                subprocess.run(
                     ["cmake", "--build", "build", f"-j{os.cpu_count() or 2}"],
                     cwd=cpp_dir,
                     check=True
                )
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