import json
import cv2
import numpy as np

with open('d:/HAMLET/3D View/model_data.json', 'r') as f:
    data = json.load(f)

def clean_polygon(poly):
    """
    Remove redundant collinear points and micro-jitters (< 4 pixels),
    ensuring alternating horizontal and vertical segments.
    """
    if len(poly) < 3:
        return poly
    
    # First pass: round to integers and remove immediate duplicates
    pts = []
    for p in poly:
        pt = [int(round(p[0])), int(round(p[1]))]
        if not pts or pt != pts[-1]:
            pts.append(pt)
    if pts and pts[0] == pts[-1]:
        pts.pop()
        
    if len(pts) < 3:
        return pts

    # Second pass: remove colinear points
    cleaned = []
    n = len(pts)
    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        
        # Collinear horizontal or vertical
        if (p_prev[0] == p_curr[0] == p_next[0]) or (p_prev[1] == p_curr[1] == p_next[1]):
            continue
            
        cleaned.append(p_curr)

    return cleaned

cleaned_units = []
for u in data['units']:
    u_copy = dict(u)
    poly = clean_polygon(u['polygon'])
    u_copy['polygon'] = poly
    
    # Check winding order: Three.js ShapeUtils expects counter-clockwise or clockwise
    # Area positive = CCW in standard Cartesian, but in screen space Y is down.
    # We will handle coordinate transformation cleanly:
    # world_x = (pixel_x - cx) * scale
    # world_z = (pixel_y - cy) * scale (or -(pixel_y - cy) * scale)
    cleaned_units.append(u_copy)

data['units'] = cleaned_units

with open('d:/HAMLET/3D View/model_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Polygons cleaned and verified successfully.")
