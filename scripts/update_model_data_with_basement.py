import json

with open('d:/HAMLET/3D View/model_data.json', 'r') as f:
    data = json.load(f)

# Add basement specifications
basement_spec = {
    "enabled": True,
    "shape": "rectangle",
    "width_m": 60.0,
    "depth_m": 96.0,
    "center_x_m": -0.58,
    "center_z_m": -2.38,
    "level_height_m": 3.2,
    "levels_count": 3,
    "levels": [
        {
            "id": "B1",
            "name": "BASEMENT LEVEL 1",
            "short_name": "B1",
            "top_y_m": 0.0,
            "bottom_y_m": -3.2,
            "height_m": 3.2,
            "elevation_label": "-3.2 m",
            "area_sqm": 5760.0,
            "area_sqft": 62000.0
        },
        {
            "id": "B2",
            "name": "BASEMENT LEVEL 2",
            "short_name": "B2",
            "top_y_m": -3.2,
            "bottom_y_m": -6.4,
            "height_m": 3.2,
            "elevation_label": "-6.4 m",
            "area_sqm": 5760.0,
            "area_sqft": 62000.0
        },
        {
            "id": "B3",
            "name": "BASEMENT LEVEL 3",
            "short_name": "B3",
            "top_y_m": -6.4,
            "bottom_y_m": -9.6,
            "height_m": 3.2,
            "elevation_label": "-9.6 m",
            "area_sqm": 5760.0,
            "area_sqft": 62000.0
        }
    ]
}

data["basement"] = basement_spec

with open('d:/HAMLET/3D View/model_data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Also update model_data.js for offline file:// support
with open('d:/HAMLET/3D View/model_data.js', 'w') as f:
    f.write('window.MODEL_DATA = ' + json.dumps(data, indent=2) + ';')

print("Updated model_data.json and model_data.js with 3-level basement specifications!")
