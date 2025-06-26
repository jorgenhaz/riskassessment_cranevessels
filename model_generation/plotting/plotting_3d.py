import numpy as np
import plotly.graph_objects as go
import os
from sympy import *
from sympy.physics.mechanics import*

# Checking matrix
def frame_matrices_are_ok (frames):
    if not isinstance(frames[0], np.ndarray):
        print("frame must be a numpy array")
        return False
    if frames[0].shape != (4, 4):
        print("Frame must be a 4x4 matrix")
        return False
    print("Frame-matrices are correct")
    return True

# Processing filepath and returns the html-code/create if file does not exists
def process_html_filepath (filepath):
    if not filepath.endswith('.html'):
        raise ValueError("FIlepath must refer to a html-file")

    fig = go.Figure()
    return fig

# Plotting reference-frame in filepath provided with matrix provided
def plot_rf_3d (frames, filepath):
    # Check T-matrix
    if not frame_matrices_are_ok(frames):
        return False
    
    folder = os.path.dirname(filepath)

    if not os.path.exists(folder):
        os.makedirs(folder, mode=0o755)

    # Check filepath
    figure = process_html_filepath(filepath)

    for T in frames:
        # Drawing X-axis
        figure.add_trace(go.Scatter3d(
            x=[T[0, 3], T[0, 3] + T[0, 0]],
            y=[T[1, 3], T[1, 3] + T[1, 0]],
            z=[T[2, 3], T[2, 3] + T[2, 0]],
            mode='lines+markers',
            line=dict(color='red', width=5),
            name='X-axis'
        ))

        # Drawing Y-axis
        figure.add_trace(go.Scatter3d(
            x=[T[0, 3], T[0, 3] + T[0, 1]],
            y=[T[1, 3], T[1, 3] + T[1, 1]],
            z=[T[2, 3], T[2, 3] + T[2, 1]],
            mode='lines+markers',
            line=dict(color='green', width=5),
            name='Y-axis'
        ))

        # Drawing Z-axis
        figure.add_trace(go.Scatter3d(
            x=[T[0, 3], T[0, 3] + T[0, 2]],
            y=[T[1, 3], T[1, 3] + T[1, 2]],
            z=[T[2, 3], T[2, 3] + T[2, 2]],
            mode='lines+markers',
            line=dict(color='blue', width=5),
            name='Z-axis'
        ))

        # Save the figure to HTML
        figure.write_html(filepath)

    os.chmod(filepath, 0o644)
    print(f"updated HTML-file: {filepath}")


def plot_3dframes (fig: go.Figure(), frames, scaler = 1) -> None:
    if not isinstance(fig, go.Figure):
        raise TypeError("Error: argument 'fig' must be an instance of plotly.graph_objects.Figure")
    
    for T in frames:
        # Drawing X-axis
        fig.add_trace(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler*T[0, 0])],
            y=[T[1, 3], (T[1, 3] + scaler*T[1, 0])],
            z=[T[2, 3], (T[2, 3] + scaler*T[2, 0])],
            mode='lines',
            line=dict(color='red', width=5),
            name='X-axis'
        ))

        # Drawing Y-axis
        fig.add_trace(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler*T[0, 1])],
            y=[T[1, 3], (T[1, 3] + scaler*T[1, 1])],
            z=[T[2, 3], (T[2, 3] + scaler*T[2, 1])],
            mode='lines',
            line=dict(color='green', width=5),
            name='Y-axis'
        ))

        # Drawing Z-axis
        fig.add_trace(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler*T[0, 2])],
            y=[T[1, 3], (T[1, 3] + scaler*T[1, 2])],
            z=[T[2, 3], (T[2, 3] + scaler*T[2, 2])],
            mode='lines',
            line=dict(color='blue', width=5),
            name='Z-axis'
        ))

"""Numpyfying sympy-functions (placed here because this is the scenario where you would use it)"""
def numpify(frames, variables):
    frame_list_numpy = [lambdify(variables, T, 'numpy') for T in frames]
    return frame_list_numpy

"""Function to substitute variables for numbers when you have a list of several matrices that have been numpified"""
def evaluate_frames(frames, values):
    frames = [T(*values) for T in frames]
    return frames


def draw_frame_line (fig: go.Figure(), T, startPoint, endPoint, color = 'black', thickness = 5, opacity=1.0) -> None:
    if not isinstance(fig, go.Figure):
        raise TypeError("Error: argument 'fig' must be an instance of plotly.graph_objects.Figure")
    
    startPoint_local = startPoint
    if len(startPoint_local) == 3:
        startPoint_local.append(1)
    elif len(startPoint_local) == 4:
        pass
    else:
        raise TypeError("Error: startPoint-argument is not correct size: ", len(startPoint_local))
    
    endPoint_local = endPoint
    if len(endPoint_local) == 3:
        endPoint_local.append(1)
    elif len(endPoint_local) == 4:
        pass
    else:
        raise TypeError("Error: startPoint-argument is not correct size: ", len(endPoint_local))
    
    startPoint_global = T @ startPoint_local
    endPoint_global = T @ endPoint_local

    line = go.Scatter3d(
        x = [startPoint_global[0], endPoint_global[0]],
        y = [startPoint_global[1], endPoint_global[1]],
        z = [startPoint_global[2], endPoint_global[2]],
        mode = 'lines',
        line = dict(color=color, width=thickness),
        opacity=opacity
    )

    fig.add_trace(line)

def plot_point (fig: go.Figure(), T, point, color = 'red', size = 4, name = '') -> None:
    if not isinstance(fig, go.Figure):
        raise TypeError("Error: argument 'fig' must be an instance of plotly.graph_objects.Figure")
    point_local = point
    if len(point_local) == 3:
        point_local.append(1)
    elif len(point_local) == 4:
        pass
    else:
        raise TypeError("Error: startPoint-argument is not correct size: ", len(point_local))
    
    point_global = T @ point_local

    marker = go.Scatter3d(
        x=[point_global[0]],
        y=[point_global[1]],
        z=[point_global[2]],
        mode='markers+text',
        marker=dict(color=color, size=size),
        text=[name],
        textposition="top center",
        name=name
    )
    fig.add_trace(marker)


def draw_prism (fig: go.Figure(), T, length, width, height, color = 'blue', opacity = 0.5, offset=np.array([0,0,0])):
    L = length/2
    W = width/2
    H = height/2

    x, y, z =compute_vertices(T, L, W, H, offset)

    faces = [
    [0, 1, 2], [0, 2, 3],  # Bunn
    [4, 5, 6], [4, 6, 7],  # Topp
    [0, 1, 5], [0, 5, 4],  # Side 1
    [1, 2, 6], [1, 6, 5],  # Side 2
    [2, 3, 7], [2, 7, 6],  # Side 3
    [3, 0, 4], [3, 4, 7]   # Side 4
    ]

        
    prism = go.Mesh3d(
        x=x, y=y, z=z,
        i=[face[0] for face in faces],
        j=[face[1] for face in faces],
        k=[face[2] for face in faces],
        color=color,
        opacity=opacity
    )

    fig.add_trace(prism)

def compute_vertices(T, L, W, H, offset=np.array([0,0,0])):


    # Define corners in local frame
    local_vertices = np.array([
        [-L, -W, -H], [L, -W, -H], [L, W, -H], [-L, W, -H],  # Bunn
        [-L, -W, H],  [L, -W, H],  [L, W, H],  [-L, W, H]     # Topp
    ]).T  # Transpose for correct shape

    # Adjust corners with center-offset argument
    local_vertices += offset.reshape(3,1)

    # Transform to global frame coordinates
    global_vertices = (T[:3, :3] @ local_vertices) + T[:3, 3].reshape(3, 1)

    return global_vertices[0], global_vertices[1], global_vertices[2]

def plot_3dframes_data(frames, scaler):
    traces = []

    for T in frames:
        traces.append(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler * T[0, 0])],
            y=[T[1, 3], (T[1, 3] + scaler * T[1, 0])],
            z=[T[2, 3], (T[2, 3] + scaler * T[2, 0])],
            mode='lines',
            line=dict(color='red', width=5),
            name='X-axis'
        ))

        traces.append(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler * T[0, 1])],
            y=[T[1, 3], (T[1, 3] + scaler * T[1, 1])],
            z=[T[2, 3], (T[2, 3] + scaler * T[2, 1])],
            mode='lines',
            line=dict(color='green', width=5),
            name='Y-axis'
        ))

        traces.append(go.Scatter3d(
            x=[T[0, 3], (T[0, 3] + scaler * T[0, 2])],
            y=[T[1, 3], (T[1, 3] + scaler * T[1, 2])],
            z=[T[2, 3], (T[2, 3] + scaler * T[2, 2])],
            mode='lines',
            line=dict(color='blue', width=5),
            name='Z-axis'
        ))

    return list(traces)  

def draw_frame_line_data(T, startPoint, endPoint, color='black'):
    startPoint_local = np.append(startPoint, 1) if len(startPoint) == 3 else startPoint
    endPoint_local = np.append(endPoint, 1) if len(endPoint) == 3 else endPoint

    startPoint_global = T @ startPoint_local
    endPoint_global = T @ endPoint_local

    return go.Scatter3d(
        x=[startPoint_global[0], endPoint_global[0]],
        y=[startPoint_global[1], endPoint_global[1]],
        z=[startPoint_global[2], endPoint_global[2]],
        mode='lines',
        line=dict(color=color, width=5)
    )

def plot_point_data(T, point, color='red', size=4, name=''):
    point_local = np.append(point, 1) if len(point) == 3 else point
    point_global = T @ point_local

    return go.Scatter3d(
        x=[point_global[0]],
        y=[point_global[1]],
        z=[point_global[2]],
        mode='markers',
        marker=dict(color=color, size=size),
        name=name,
        showlegend=True
    )

def draw_prism_data(T, length, width, height, color='blue', opacity=0.5, offset=np.array([0, 0, 0])):
    L, W, H = length / 2, width / 2, height / 2
    x, y, z = compute_vertices(T, L, W, H, offset)

    faces = [
        [0, 1, 2], [0, 2, 3],  # Bottom
        [4, 5, 6], [4, 6, 7],  # Top
        [0, 1, 5], [0, 5, 4],  # Side 1
        [1, 2, 6], [1, 6, 5],  # Side 2
        [2, 3, 7], [2, 7, 6],  # Side 3
        [3, 0, 4], [3, 4, 7]   # Side 4
    ]

    return go.Mesh3d(
        x=x, y=y, z=z,
        i=[face[0] for face in faces],
        j=[face[1] for face in faces],
        k=[face[2] for face in faces],
        color=color,
        opacity=opacity,
        name = 'Prism',
        showlegend=True
    )

def draw_text_in_frame(fig: go.Figure, T, local_position, text, color='black', size=12, name='Text'):
    if len(local_position) == 3:
        local_position = np.append(local_position, 1)
    elif len(local_position) != 4:
        raise ValueError("Position must be length 3 or 4.")

    global_position = T @ local_position

    fig.add_trace(go.Scatter3d(
        x=[global_position[0]],
        y=[global_position[1]],
        z=[global_position[2]],
        mode='text',
        text=[text],
        textposition='top center',
        textfont=dict(color=color, size=size),
        name=name,
        showlegend=False
    ))

def draw_arrow(fig: go.Figure, T, origin, direction, color='black', shaft_width=5, head_length=0.05):
    """
    Tegner en pil som peker mot 'origin' fra 'origin + direction', transformert med T.
    """
    # Lokalpunkter
    end_local = np.append(origin, 1)
    start_local = np.append(np.array(origin) + np.array(direction), 1)

    # Globale punkter
    start_global = T @ start_local
    end_global = T @ end_local

    # Retning
    head_dir = end_global[:3] - start_global[:3]
    norm = np.linalg.norm(head_dir)
    if norm < 1e-8:
        return  # Ikke tegn pil – den har ingen retning
    head_dir = head_dir / norm
    head_base = end_global[:3] - head_length * head_dir
    head_tip = end_global[:3]

    # Skaft
    fig.add_trace(go.Scatter3d(
        x=[start_global[0], head_base[0]],
        y=[start_global[1], head_base[1]],
        z=[start_global[2], head_base[2]],
        mode='lines',
        line=dict(color=color, width=shaft_width),
        showlegend=False
    ))

    # Pilhode
    ortho = np.cross(head_dir, [0, 0, 1])
    if np.linalg.norm(ortho) < 1e-3:
        ortho = np.cross(head_dir, [0, 1, 0])
    ortho = ortho / np.linalg.norm(ortho)

    scale = head_length * 0.4
    base1 = head_base + scale * ortho
    base2 = head_base - scale * ortho

    fig.add_trace(go.Mesh3d(
        x=[head_tip[0], base1[0], base2[0]],
        y=[head_tip[1], base1[1], base2[1]],
        z=[head_tip[2], base1[2], base2[2]],
        i=[0], j=[1], k=[2],
        color=color,
        opacity=1.0,
        showlegend=False
    ))


def draw_curved_arrow(fig: go.Figure, T_start, T_end, color='black', shaft_width=4, head_length=0.05, steps=50, curve_height=0.15):
    """
    Tegner en kurvet pil fra z-aksen på T_start til z-aksen på T_end.
    """
    # Start- og sluttpunkt på Z-aksene
    p0 = T_start[:3, 3] + T_start[:3, 2] * 0.3
    p1 = T_end[:3, 3] + T_end[:3, 2] * 0.3

    # Løft buen opp i Z-retning for å gjøre den synlig
    mid = (p0 + p1) / 2 + np.array([0, 0, curve_height])

    # Bézier-kurve
    t = np.linspace(0, 1, steps)
    bezier = (
        (1 - t)[:, None]**2 * p0 +
        2 * (1 - t)[:, None] * t[:, None] * mid +
        t[:, None]**2 * p1
    )

    # Tegn skaftet
    fig.add_trace(go.Scatter3d(
        x=bezier[:, 0],
        y=bezier[:, 1],
        z=bezier[:, 2],
        mode='lines',
        line=dict(color=color, width=shaft_width),
        showlegend=False
    ))

    # Pilhode i enden
    head_tip = bezier[-1]
    head_base = bezier[-2]

    head_dir = head_tip - head_base
    head_dir = head_dir / np.linalg.norm(head_dir)

    ortho = np.cross(head_dir, [1, 0, 0])
    if np.linalg.norm(ortho) < 1e-3:
        ortho = np.cross(head_dir, [0, 1, 0])
    ortho = ortho / np.linalg.norm(ortho)

    scale = head_length * 0.4
    base1 = head_base + scale * ortho
    base2 = head_base - scale * ortho

    fig.add_trace(go.Mesh3d(
        x=[head_tip[0], base1[0], base2[0]],
        y=[head_tip[1], base1[1], base2[1]],
        z=[head_tip[2], base1[2], base2[2]],
        i=[0], j=[1], k=[2],
        color=color,
        opacity=1.0,
        showlegend=False
    ))
