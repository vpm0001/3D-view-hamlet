import cv2
import numpy as np
import json
import os

IMAGE_PATH = 'd:/HAMLET/3D View/source_images/floor_plan_1446x2048.png'
img = cv2.imread(IMAGE_PATH)
h_img, w_img, _ = img.shape

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
apt_mask = ((hsv[:, :, 1] > 8) & (gray < 248)).astype(np.uint8) * 255
wall_mask = (gray < 75).astype(np.uint8) * 255

UNITS_CONFIG = [
    # Cluster 1: Top-Left
    {"id": "APT_15", "name": "TYPE 15", "type": "1BHK+1T", "area": 741.26, "cluster": "top_left", "is_core": False, "bbox": [150, 60, 375, 272]},
    {"id": "APT_12_TL", "name": "TYPE 12", "type": "1BHK+1T", "area": 686.81, "cluster": "top_left", "is_core": False, "bbox": [150, 260, 375, 355]},
    {"id": "STAIR_1", "name": "STAIR CORE 01", "type": "STAIR", "area": 0, "cluster": "top_left", "is_core": True, "bbox": [188, 345, 358, 435]},
    {"id": "APT_14", "name": "TYPE 14", "type": "1BHK+1T", "area": 731.36, "cluster": "top_left", "is_core": False, "bbox": [150, 428, 375, 528]},
    {"id": "APT_04", "name": "TYPE 04", "type": "3BHK+2T", "area": 1686.20, "cluster": "top_left", "is_core": False, "bbox": [150, 520, 375, 830]},

    # Cluster 2: Upper Mid
    {"id": "APT_06", "name": "TYPE 06", "type": "3BHK+2T", "area": 1455.61, "cluster": "upper_mid", "is_core": False, "bbox": [375, 135, 600, 365]},
    {"id": "APT_10", "name": "TYPE 10", "type": "2BHK+2T", "area": 1057.17, "cluster": "upper_mid", "is_core": False, "bbox": [375, 360, 610, 565]},
    {"id": "STAIR_LIFT_2", "name": "STAIR & LIFT CORE 02", "type": "CORE", "area": 0, "cluster": "upper_mid", "is_core": True, "bbox": [615, 395, 805, 565]},
    {"id": "APT_13_UM", "name": "TYPE 13", "type": "1BHK+1T", "area": 721.24, "cluster": "upper_mid", "is_core": False, "bbox": [790, 355, 955, 485]},
    {"id": "APT_05", "name": "TYPE 05", "type": "3BHK+2T", "area": 1386.64, "cluster": "upper_mid", "is_core": False, "bbox": [905, 360, 1200, 565]},

    # Cluster 3: Middle Horizontal Row
    {"id": "APT_11_M1", "name": "TYPE 11", "type": "1BHK+1T", "area": 697.25, "cluster": "mid_row", "is_core": False, "bbox": [385, 580, 532, 805]},
    {"id": "APT_12_M1", "name": "TYPE 12", "type": "1BHK+1T", "area": 688.64, "cluster": "mid_row", "is_core": False, "bbox": [528, 580, 668, 805]},
    {"id": "APT_11_M2", "name": "TYPE 11", "type": "1BHK+1T", "area": 688.64, "cluster": "mid_row", "is_core": False, "bbox": [662, 580, 802, 805]},
    {"id": "APT_12_M2", "name": "TYPE 12", "type": "1BHK+1T", "area": 697.25, "cluster": "mid_row", "is_core": False, "bbox": [798, 580, 942, 805]},

    # Cluster 4: East Stack
    {"id": "APT_11_E1", "name": "TYPE 11", "type": "1BHK+1T", "area": 697.25, "cluster": "east_stack", "is_core": False, "bbox": [965, 575, 1180, 725]},
    {"id": "APT_11_E2", "name": "TYPE 11", "type": "1BHK+1T", "area": 697.25, "cluster": "east_stack", "is_core": False, "bbox": [965, 715, 1180, 865]},

    # Cluster 5: Center & Stair 3
    {"id": "APT_08_C", "name": "TYPE 08", "type": "2BHK+2T", "area": 1126.68, "cluster": "center", "is_core": False, "bbox": [710, 845, 955, 1035]},
    {"id": "STAIR_3", "name": "STAIR CORE 03", "type": "STAIR", "area": 0, "cluster": "center", "is_core": True, "bbox": [965, 875, 1120, 980]},
    {"id": "APT_11_SE", "name": "TYPE 11", "type": "1BHK+1T", "area": 696.81, "cluster": "center", "is_core": False, "bbox": [950, 970, 1180, 1125]},
    {"id": "APT_09_SE", "name": "TYPE 09", "type": "2BHK+2T", "area": 1157.02, "cluster": "center", "is_core": False, "bbox": [950, 1105, 1200, 1310]},

    # Cluster 6: Lower Left
    {"id": "APT_13_LL", "name": "TYPE 13", "type": "1BHK+1T", "area": 772.78, "cluster": "lower_left", "is_core": False, "bbox": [270, 1095, 422, 1285]},
    {"id": "APT_12_LL", "name": "TYPE 12", "type": "1BHK+1T", "area": 686.81, "cluster": "lower_left", "is_core": False, "bbox": [418, 1095, 538, 1285]},
    {"id": "STAIR_4", "name": "STAIR CORE 04", "type": "STAIR", "area": 0, "cluster": "lower_left", "is_core": True, "bbox": [520, 1135, 645, 1295]},
    {"id": "APT_03", "name": "TYPE 03", "type": "3BHK+2T", "area": 1526.52, "cluster": "lower_left", "is_core": False, "bbox": [650, 1075, 935, 1315]},
    {"id": "APT_09_BL1", "name": "TYPE 09", "type": "2BHK+2T", "area": 1157.02, "cluster": "lower_left", "is_core": False, "bbox": [320, 1330, 532, 1565]},
    {"id": "APT_09_BL2", "name": "TYPE 09", "type": "2BHK+2T", "area": 1157.02, "cluster": "lower_left", "is_core": False, "bbox": [518, 1330, 722, 1565]},

    # Cluster 7: Lower Right
    {"id": "APT_08_BR", "name": "TYPE 08", "type": "2BHK+2T", "area": 1123.88, "cluster": "lower_right", "is_core": False, "bbox": [810, 1330, 1035, 1515]},
    {"id": "APT_02", "name": "TYPE 02", "type": "3BHK+2T", "area": 1502.43, "cluster": "lower_right", "is_core": False, "bbox": [825, 1495, 1055, 1805]},
    {"id": "STAIR_LIFT_5", "name": "STAIR & LIFT CORE 05", "type": "CORE", "area": 0, "cluster": "lower_right", "is_core": True, "bbox": [1025, 1330, 1260, 1435]},
    {"id": "APT_07", "name": "TYPE 07", "type": "2BHK+2T", "area": 1091.60, "cluster": "lower_right", "is_core": False, "bbox": [1050, 1415, 1275, 1625]},
    {"id": "APT_01", "name": "TYPE 01", "type": "3BHK+2T", "area": 1541.37, "cluster": "lower_right", "is_core": False, "bbox": [1050, 1605, 1275, 1920]}
]

def make_orthogonal(poly):
    """Ensure all polygon segments are strictly horizontal or vertical."""
    n = len(poly)
    if n < 3:
        return poly
    res = []
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        res.append([int(p1[0]), int(p1[1])])
        if dx > 4 and dy > 4:
            # Need an intermediate orthogonal corner
            # Check orientation
            corner = [int(p2[0]), int(p1[1])]
            res.append(corner)
    
    # Clean up redundant colinear points
    cleaned = []
    for i in range(len(res)):
        p_prev = res[i - 1]
        p_curr = res[i]
        p_next = res[(i + 1) % len(res)]
        # Check if colinear horizontal or vertical
        if (p_prev[0] == p_curr[0] == p_next[0]) or (p_prev[1] == p_curr[1] == p_next[1]):
            continue
        cleaned.append(p_curr)
    return cleaned

extracted_units = []

for cfg in UNITS_CONFIG:
    x1, y1, x2, y2 = cfg["bbox"]
    unit_id = cfg["id"]
    is_core = cfg["is_core"]
    
    if is_core:
        # Extract core box from dark walls
        crop = wall_mask[y1:y2, x1:x2]
        cnts, _ = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        all_pts = []
        for c in cnts:
            if cv2.contourArea(c) > 15:
                for pt in c:
                    all_pts.append(pt[0])
        if all_pts:
            all_pts = np.array(all_pts)
            bx, by, bw, bh = cv2.boundingRect(all_pts)
            # Core polygon
            poly = [
                [x1 + bx, y1 + by],
                [x1 + bx + bw, y1 + by],
                [x1 + bx + bw, y1 + by + bh],
                [x1 + bx, y1 + by + bh]
            ]
        else:
            poly = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    else:
        crop = apt_mask[y1:y2, x1:x2]
        kernel = np.ones((7, 7), np.uint8)
        closed = cv2.morphologyEx(crop, cv2.MORPH_CLOSE, kernel)
        cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            approx = cv2.approxPolyDP(c, 0.012 * cv2.arcLength(c, True), True)
            raw_pts = approx.reshape(-1, 2) + np.array([x1, y1])
            poly = make_orthogonal(raw_pts.tolist())
        else:
            poly = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]

    unit_record = dict(cfg)
    unit_record["polygon"] = poly
    extracted_units.append(unit_record)
    print(f"Extracted {unit_id}: {len(poly)} vertices")

# Save to JSON
with open('d:/HAMLET/3D View/model_data.json', 'w') as f:
    json.dump({
        "image_width": 1446,
        "image_height": 2048,
        "floor_height_m": 3.2,
        "units": extracted_units
    }, f, indent=2)

print("Saved model_data.json successfully!")

# Generate overlay verification image
overlay_img = img.copy()
for u in extracted_units:
    poly = np.array(u["polygon"], dtype=np.int32)
    is_core = u["is_core"]
    color = (60, 60, 60) if is_core else (240, 220, 180) # BGR
    border = (0, 0, 180) if is_core else (255, 50, 0)
    
    cv2.fillPoly(overlay_img, [poly], color)
    cv2.polylines(overlay_img, [poly], True, border, 2)
    
    # Label
    cx = int(np.mean(poly[:, 0]))
    cy = int(np.mean(poly[:, 1]))
    cv2.putText(overlay_img, u["name"], (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

# Blend overlay with original
blended = cv2.addWeighted(overlay_img, 0.6, img, 0.4, 0)
cv2.imwrite('d:/HAMLET/3D View/source_images/verification_overlay.png', blended)
print("Saved verification_overlay.png successfully!")
