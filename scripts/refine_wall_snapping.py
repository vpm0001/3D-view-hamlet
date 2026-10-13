import cv2
import numpy as np
import json

img = cv2.imread('d:/HAMLET/3D View/source_images/floor_plan_1446x2048.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
wall = (gray < 85).astype(np.uint8)

with open('d:/HAMLET/3D View/model_data.json') as f:
    data = json.load(f)

def snap_coordinate(coord, is_x, search_window=8):
    """
    Search nearby lines (+/- search_window) for the strongest wall line peak.
    """
    best_c = coord
    best_weight = 0
    for offset in range(-search_window, search_window + 1):
        c = coord + offset
        if is_x:
            if 0 <= c < img.shape[1]:
                weight = np.sum(wall[:, c])
        else:
            if 0 <= c < img.shape[0]:
                weight = np.sum(wall[c, :])
        if weight > best_weight:
            best_weight = weight
            best_c = c
    return best_c

print("Testing wall snapping...")
