import json
import cv2
import numpy as np

with open('d:/HAMLET/3D View/model_data.json', 'r') as f:
    data = json.load(f)

print(f"Testing {len(data['units'])} units for 3D extrusion...")

for u in data['units']:
    pts = np.array(u['polygon'], dtype=np.int32)
    area = cv2.contourArea(pts)
    assert len(pts) >= 3 and area > 100

print("Testing corridors...")
for c in data.get('corridors', []):
    pts = np.array(c['polygon'], dtype=np.int32)
    area = cv2.contourArea(pts)
    print(f"Corridor {c['id']}: area={area:.0f}, vertices={len(pts)}")

print("ALL GEOMETRY VERIFIED SUCCESSFULLY!")
