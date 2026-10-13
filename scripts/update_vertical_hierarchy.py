import json

with open('d:/HAMLET/3D View/model_data.json', 'r') as f:
    data = json.load(f)

# Define the complete building vertical hierarchy
FLOOR_HEIGHT = 3.2

floors_meta = [
    # Substructure
    {"id": "B3", "name": "BASEMENT 3", "type": "basement", "level_index": -3, "elevation_m": -9.6, "top_y_m": -6.4, "bot_y_m": -9.6},
    {"id": "B2", "name": "BASEMENT 2", "type": "basement", "level_index": -2, "elevation_m": -6.4, "top_y_m": -3.2, "bot_y_m": -6.4},
    {"id": "B1", "name": "BASEMENT 1", "type": "basement", "level_index": -1, "elevation_m": -3.2, "top_y_m": 0.0, "bot_y_m": -3.2},
    # Ground Floor
    {"id": "G", "name": "GROUND FLOOR", "type": "ground", "level_index": 0, "elevation_m": 0.0, "top_y_m": 3.2, "bot_y_m": 0.0},
    # 14 Residential Floors
    {"id": "1F", "name": "1ST FLOOR", "type": "residential", "level_index": 1, "elevation_m": 3.2, "top_y_m": 6.4, "bot_y_m": 3.2},
    {"id": "2F", "name": "2ND FLOOR", "type": "residential", "level_index": 2, "elevation_m": 6.4, "top_y_m": 9.6, "bot_y_m": 6.4},
    {"id": "3F", "name": "3RD FLOOR", "type": "residential", "level_index": 3, "elevation_m": 9.6, "top_y_m": 12.8, "bot_y_m": 9.6},
    {"id": "4F", "name": "4TH FLOOR", "type": "residential", "level_index": 4, "elevation_m": 12.8, "top_y_m": 16.0, "bot_y_m": 12.8},
    {"id": "5F", "name": "5TH FLOOR", "type": "residential", "level_index": 5, "elevation_m": 16.0, "top_y_m": 19.2, "bot_y_m": 16.0},
    {"id": "6F", "name": "6TH FLOOR", "type": "residential", "level_index": 6, "elevation_m": 19.2, "top_y_m": 22.4, "bot_y_m": 19.2},
    {"id": "7F", "name": "7TH FLOOR", "type": "residential", "level_index": 7, "elevation_m": 22.4, "top_y_m": 25.6, "bot_y_m": 22.4},
    {"id": "8F", "name": "8TH FLOOR", "type": "residential", "level_index": 8, "elevation_m": 25.6, "top_y_m": 28.8, "bot_y_m": 25.6},
    {"id": "9F", "name": "9TH FLOOR", "type": "residential", "level_index": 9, "elevation_m": 28.8, "top_y_m": 32.0, "bot_y_m": 28.8},
    {"id": "10F", "name": "10TH FLOOR", "type": "residential", "level_index": 10, "elevation_m": 32.0, "top_y_m": 35.2, "bot_y_m": 32.0},
    {"id": "11F", "name": "11TH FLOOR", "type": "residential", "level_index": 11, "elevation_m": 35.2, "top_y_m": 38.4, "bot_y_m": 35.2},
    {"id": "12F", "name": "12TH FLOOR", "type": "residential", "level_index": 12, "elevation_m": 38.4, "top_y_m": 41.6, "bot_y_m": 38.4},
    {"id": "13F", "name": "13TH FLOOR", "type": "residential", "level_index": 13, "elevation_m": 41.6, "top_y_m": 44.8, "bot_y_m": 41.6},
    {"id": "14F", "name": "14TH FLOOR", "type": "residential", "level_index": 14, "elevation_m": 44.8, "top_y_m": 48.0, "bot_y_m": 44.8}
]

building_hierarchy = {
    "floor_height_m": FLOOR_HEIGHT,
    "total_above_ground_levels": 15, # Ground + 14
    "residential_levels_count": 14,  # 1st to 14th
    "basement_levels_count": 3,      # B1, B2, B3
    "total_height_m": 48.0,
    "total_underground_depth_m": 9.6,
    "floors": floors_meta
}

data["vertical_structure"] = building_hierarchy

with open('d:/HAMLET/3D View/model_data.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('d:/HAMLET/3D View/model_data.js', 'w') as f:
    f.write('window.MODEL_DATA = ' + json.dumps(data, indent=2) + ';')

print("Updated model_data.json and model_data.js with complete G+14 building vertical hierarchy!")
