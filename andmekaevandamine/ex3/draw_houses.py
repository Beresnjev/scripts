import json
import matplotlib.pyplot as plt
import numpy as np
import os


# Function to load polygon coordinates from a JSON file
def load_polygon_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Extracting the first polygon's coordinates
    base_object = data[0]["ehitis"]["ehitiseKujud"]["ruumikuju"][0]
    return base_object["geometry"]["coordinates"][0], base_object["taisaadress"]


# Function to rotate a point around another point
def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return [qx, qy]


# Function to calculate the angle to rotate the polygon
def angle_to_rotate_polygon(coords):
    max_length = 0
    angle_of_longest_edge = 0
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        length = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        if length > max_length:
            max_length = length
            angle_of_longest_edge = np.arctan2((p2[1] - p1[1]), (p2[0] - p1[0]))
    return -angle_of_longest_edge


def draw_plot(file):
    # Load polygon coordinates from JSON file
    polygon_coords, address = load_polygon_from_json(file)
    building_id = os.path.basename(file).replace(".ehr.json", "")

    # Calculate the angle needed to rotate the polygon
    angle = angle_to_rotate_polygon(polygon_coords)

    # Choose the first vertex of the longest edge as the origin for rotation
    origin = polygon_coords[0]

    # Rotate the polygon
    rotated_polygon_coords = [rotate_point(origin, point, angle) for point in polygon_coords]

    # Transform the rotated polygon so the minimums for both axes are 0
    min_x_rotated = min(coord[0] for coord in rotated_polygon_coords)
    min_y_rotated = min(coord[1] for coord in rotated_polygon_coords)
    transformed_rotated_coords = [[x - min_x_rotated, y - min_y_rotated] for x, y in rotated_polygon_coords]

    # Plotting the transformed and rotated polygon
    x_transformed_rotated, y_transformed_rotated = zip(*transformed_rotated_coords)
    plt.figure()
    plt.fill(x_transformed_rotated, y_transformed_rotated, 'b', alpha=0.5)
    plt.plot(x_transformed_rotated, y_transformed_rotated, 'r-')
    plt.title(f"Top-down view of building {building_id} \n({address})")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.axis('equal')
    output_file = os.path.join("plots", os.path.basename(file).replace(".json", ".png"))
    plt.savefig(output_file)
    plt.close()


building_ids = [
        "120530679", "120530734", "120530759",  # Meeliku
        "120643546", "120643547", "120643548",  # Pallasti
        "101010836", "101011193", "101013480",  # Kärberi
        "114012183", "114012184", "114012196",  # Tartu mnt
    ]

for building_id in building_ids:
    draw_plot(f"{building_id}.ehr.json")
