import json
import numpy as np

# Let's define the continuous corridor network based on the floor plan circulation:
# The corridors connect all unit entries and stair cores:
corridors = [
    # 1. Top-Left Vertical Corridor (along Type 15, 12, Stair 1, 14, 04)
    # X: 355 to 395, Y: 140 to 590
    {
        "id": "CORR_TL_VERT",
        "name": "North-West Corridor",
        "polygon": [
            [354, 140],
            [392, 140],
            [392, 590],
            [354, 590]
        ]
    },
    # 2. Main Middle Horizontal Corridor (between Upper cluster / Type 06, 10, Stair 2 and Middle Row)
    # X: 354 to 975, Y: 525 to 592
    {
        "id": "CORR_MID_HORIZ",
        "name": "Central Spine Corridor",
        "polygon": [
            [354, 525],
            [975, 525],
            [975, 592],
            [354, 592]
        ]
    },
    # 3. Upper Middle Spur to Stair 2 & Lifts & Type 13/05
    # X: 590 to 950, Y: 460 to 535
    {
        "id": "CORR_UPPER_SPUR",
        "name": "North Core Corridor",
        "polygon": [
            [590, 465],
            [950, 465],
            [950, 530],
            [590, 530]
        ]
    },
    # 4. East Vertical Corridor (along East stack Type 11, 11 and Center Stair 3)
    # X: 930 to 975, Y: 585 to 1340
    {
        "id": "CORR_EAST_VERT",
        "name": "East Circulation Corridor",
        "polygon": [
            [930, 585],
            [975, 585],
            [975, 1340],
            [930, 1340]
        ]
    },
    # 5. Lower Left Horizontal Corridor (between Type 13/12/Stair 4/03 and Type 09 bl1/bl2)
    # X: 275 to 940, Y: 1280 to 1340
    {
        "id": "CORR_LL_HORIZ",
        "name": "South-West Corridor",
        "polygon": [
            [275, 1280],
            [940, 1280],
            [940, 1340],
            [275, 1340]
        ]
    },
    # 6. Lower Right Vertical Corridor (between Type 08/02 and Stair 5/Type 07/01)
    # X: 1030 to 1070, Y: 1335 to 1620
    {
        "id": "CORR_LR_VERT",
        "name": "South-East Corridor",
        "polygon": [
            [1030, 1335],
            [1070, 1335],
            [1070, 1620],
            [1030, 1620]
        ]
    }
]

# Update model_data.json with corridors
with open('d:/HAMLET/3D View/model_data.json', 'r') as f:
    data = json.load(f)

data["corridors"] = corridors

with open('d:/HAMLET/3D View/model_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(corridors)} corridor segments to model_data.json")
