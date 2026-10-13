import cv2
import numpy as np
import json

img = cv2.imread('d:/HAMLET/3D View/source_images/floor_plan_1446x2048.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
wall = (gray < 85).astype(np.uint8) * 255

# Distance transform: distance from every pixel to nearest dark CAD wall pixel
dist_to_wall = cv2.distanceTransform(255 - wall, cv2.DIST_L2, 3)

with open('d:/HAMLET/3D View/model_data.json') as f:
    data = json.load(f)

print("Evaluating polygon edge alignment to CAD walls:")
scores = []
for u in data['units']:
    poly = np.array(u['polygon'], dtype=np.int32)
    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.polylines(mask, [poly], True, 255, 1)
    edge_pts = np.where(mask > 0)
    avg_dist = float(np.mean(dist_to_wall[edge_pts]))
    scores.append(avg_dist)
    print(f"{u['id']:<15} | avg distance to nearest CAD wall: {avg_dist:.2f} px")

print(f"\nOVERALL MEAN ALIGNMENT DISTANCE: {np.mean(scores):.2f} pixels!")
