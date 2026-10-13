import cv2
import numpy as np
import json

IMAGE_PATH = 'd:/HAMLET/3D View/source_images/floor_plan_1446x2048.png'
base_img = cv2.imread(IMAGE_PATH)
h, w, _ = base_img.shape

with open('d:/HAMLET/3D View/model_data.json') as f:
    data = json.load(f)

# Create a clean architectural 2D massing rendering matching the 3D top view
massing_canvas = np.ones((h, w, 3), dtype=np.uint8) * 233 # light grey background (#e9eaed)

# 1. Draw Corridors
for c in data.get('corridors', []):
    poly = np.array(c['polygon'], dtype=np.int32)
    # Fill corridor with slightly darker neutral grey (#c6c9ce)
    cv2.fillPoly(massing_canvas, [poly], (206, 201, 198)) # BGR
    cv2.polylines(massing_canvas, [poly], True, (166, 161, 154), 1)

# 2. Draw Apartments & Stair Cores
for u in data['units']:
    poly = np.array(u['polygon'], dtype=np.int32)
    is_core = u['is_core']
    
    if is_core:
        # Dark charcoal grey (#35393d -> BGR: 61, 57, 53)
        fill_color = (61, 57, 53)
        edge_color = (23, 21, 20)
    else:
        # Ivory / off-white (#f4f1ea -> BGR: 234, 241, 244)
        fill_color = (234, 241, 244)
        edge_color = (41, 38, 36)
        
    cv2.fillPoly(massing_canvas, [poly], fill_color)
    cv2.polylines(massing_canvas, [poly], True, edge_color, 2)
    
    # Label center
    cx = int(np.mean(poly[:, 0]))
    cy = int(np.mean(poly[:, 1]))
    text_color = (255, 255, 255) if is_core else (40, 40, 40)
    font_scale = 0.38 if is_core else 0.42
    cv2.putText(massing_canvas, u['name'], (cx - 28, cy), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 1, cv2.LINE_AA)

# Save massing 2D render
cv2.imwrite('d:/HAMLET/3D View/source_images/massing_top_view.png', massing_canvas)

# Create 50% blended overlay onto source floor plan
blended = cv2.addWeighted(massing_canvas, 0.55, base_img, 0.45, 0)
cv2.imwrite('d:/HAMLET/3D View/source_images/comparison_overlay.png', blended)

# Create side-by-side comparison image
# Scale both down to height 1024 for quick viewing
s_base = cv2.resize(base_img, (int(w * 1024 / h), 1024))
s_mass = cv2.resize(massing_canvas, (int(w * 1024 / h), 1024))
side_by_side = np.hstack([s_base, s_mass])
cv2.imwrite('d:/HAMLET/3D View/source_images/comparison_side_by_side.png', side_by_side)

print("Generated validation comparison images successfully!")
