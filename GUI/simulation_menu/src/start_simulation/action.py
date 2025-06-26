import subprocess, sys, os, threading
import pyglet
def start_simulation_action(self, widget):
    print("Start simulation action...")
    self.current_view.status.text = "Simulating..."
    self.current_view.status.color = (255, 0, 0, 255)
    self.current_view.status.visible = True

    def worker():
        try:
            result = subprocess.run(
                ["cpp_gui/build/my_program"],  
                check=True,                  
                stdout=subprocess.PIPE,     
                stderr=subprocess.PIPE,     
                text=True                    
            )
            print("Program output:\n", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error while running program:")
            print(e.stderr)

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