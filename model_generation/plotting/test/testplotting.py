import numpy as np
import os
from plotting.plotting_3d import plot_rf_3d

frame_list = []

frame_1 = np.array([[1, 0, 0, 0],    # x-aksens retning og posisjon (kolonne 1)
              [0, 1, 0, 0],    # y-aksens retning og posisjon (kolonne 2)
              [0, 0, 1, 0],    # z-aksens retning og posisjon (kolonne 3)
              [0, 0, 0, 1]])   # homogenitet
frame_list.append(frame_1)

frame_2 = np.array([[1, 0, 0, 2],    # x-aksens retning og posisjon (kolonne 1)
              [0, 1, 0, 3],    # y-aksens retning og posisjon (kolonne 2)
              [0, 0, 1, 4],    # z-aksens retning og posisjon (kolonne 3)
              [0, 0, 0, 1]])   # homogenitet
frame_list.append(frame_2)

frame_3 = np.array([[1, 0, 0, 10],    # x-aksens retning og posisjon (kolonne 1)
              [0, 1, 0, 7],    # y-aksens retning og posisjon (kolonne 2)
              [0, 0, 1, 7],    # z-aksens retning og posisjon (kolonne 3)
              [0, 0, 0, 1]])   # homogenitet
frame_list.append(frame_3)

folder_path = "../../outputfolder"
file_path = os.path.join(folder_path, "test_8.html")

plot_rf_3d(frame_list, file_path)
