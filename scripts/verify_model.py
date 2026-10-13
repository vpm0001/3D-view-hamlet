import json
import cv2
import numpy as np

with open('d:/HAMLET/3D View/model_data.json') as f:
    data = json.load(f)

print(f"Total units in model_data.json: {len(data['units'])}")

# Check areas and bounds of all units
for u in data['units']:
    poly = np.array(u['polygon'])
    x_min, y_min = np.min(poly, axis=0)
    x_max, y_max = np.max(poly, axis=0)
    # calculate polygon area using cv2.contourArea
    area = cv2.contourArea(poly)
    print(f"{u['id']:<15} | {u['name']:<12} | Core:{str(u['is_core']):<5} | Verts:{len(poly):<2} | Bounds: X:[{x_min:4d}, {x_max:4d}] Y:[{y_min:4d}, {y_max:4d}] | Area:{area:8.0f}")
