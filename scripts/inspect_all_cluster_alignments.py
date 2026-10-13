import cv2
import numpy as np
import json

# Load base image and model data
img = cv2.imread('d:/HAMLET/3D View/source_images/floor_plan_1446x2048.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Wall edges
wall_mask = (gray < 80).astype(np.uint8)

with open('d:/HAMLET/3D View/model_data.json') as f:
    data = json.load(f)

print(f"Checking {len(data['units'])} units...")

# For each cluster, let's crop and save a high-res inspection image showing the polygon edges in red over the CAD walls
clusters = {}
for u in data['units']:
    c_name = u['cluster']
    clusters.setdefault(c_name, []).append(u)

for c_name, units in clusters.items():
    # Find bounding box of all units in cluster
    all_pts = []
    for u in units:
        all_pts.extend(u['polygon'])
    all_pts = np.array(all_pts)
    x_min = max(0, np.min(all_pts[:, 0]) - 30)
    x_max = min(img.shape[1], np.max(all_pts[:, 0]) + 30)
    y_min = max(0, np.min(all_pts[:, 1]) - 30)
    y_max = min(img.shape[0], np.max(all_pts[:, 1]) + 30)
    
    crop = img[y_min:y_max, x_min:x_max].copy()
    overlay = crop.copy()
    
    for u in units:
        poly = np.array(u['polygon']) - np.array([x_min, y_min])
        color = (80, 80, 80) if u['is_core'] else (240, 230, 210)
        border = (0, 0, 220) if u['is_core'] else (220, 20, 0)
        cv2.fillPoly(overlay, [poly], color)
        cv2.polylines(crop, [poly], True, border, 2)
        
        # Centroid
        cx = int(np.mean(poly[:, 0]))
        cy = int(np.mean(poly[:, 1]))
        cv2.putText(crop, u['name'], (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
        
    blended = cv2.addWeighted(overlay, 0.4, crop, 0.6, 0)
    out_path = f'd:/HAMLET/3D View/source_images/inspect_{c_name}.png'
    cv2.imwrite(out_path, blended)
    print(f"Saved inspection crop for cluster: {c_name} (X:[{x_min},{x_max}], Y:[{y_min},{y_max}])")

print("All cluster inspection crops generated.")
