import csv
import pyglet
import pandas as pd
from pathlib import Path
import numpy as np
import yaml
from GUI.utils.popup.message_popup import MessagePopup

def plot_simulation_action(self_window_ptr, widget, self_ptr):
    print("Evaluating data")

    project_root = Path.cwd()

    with open(project_root/'cpp_gui/files/sim_args.yaml', 'r') as file:
        params = yaml.safe_load(file)

    csv_file = params['file_name']

    df = pd.read_csv(project_root/csv_file)
    max_roll_deg            = (np.rad2deg(abs(max(df['phi']))))
    max_pitch_deg           = (np.rad2deg(abs(max(df['theta']))))
    max_heave_variation     = abs(max(df['z']) - min(df['z']))
    
    lines = [
        "Significant wave height: 0.5",
        "Wave period: 4.0",
        f"Max roll  : {max_roll_deg:.1f}°",
        f"Max pitch : {max_pitch_deg:.1f}°",
        f"Max heave-variation : {max_heave_variation:.2f} m",
        "Click or Esc to close",
        "Volume aft stb ballast: 1000",
        "Volume aft ps ballast: 1200",
        "Volume fp stb ballast: 1200",
        "Volume fp ps ballast: 1100",
        "Min freeboard: 0.9"
    ]

    popup = MessagePopup(self_window_ptr, lines, title="Simulation stats")
    self_window_ptr.push_handlers(popup)   
    self_window_ptr.invalid = True
