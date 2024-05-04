import json
import numpy as np
from shapely.geometry import Polygon


# Функция для вычисления площади многоугольника по его координатам
def polygon_area(coordinates):
    polygon = Polygon(coordinates)
    return polygon.area


# Функция для вычисления периметра многоугольника по его координатам
def polygon_perimeter(coordinates):
    polygon = Polygon(coordinates)
    return polygon.length


# Функция для сравнения двух домов по площади и форме
def compare_houses(house1, house2):
    area1 = polygon_area(house1)
    area2 = polygon_area(house2)

    perimeter1 = polygon_perimeter(house1)
    perimeter2 = polygon_perimeter(house2)

    # Вычисляем отношение периметра к площади для каждого дома
    compactness1 = perimeter1 / np.sqrt(area1)
    compactness2 = perimeter2 / np.sqrt(area2)

    # Вычисляем аспектное отношение для каждого дома
    aspect_ratio1 = max(np.sqrt(area1) / np.sqrt(area2), np.sqrt(area2) / np.sqrt(area1))

    # Вычисляем разницу в площади, периметре и аспектном отношении с учетом весов
    weight_area = 0.4
    weight_compactness = 0.3
    weight_aspect_ratio = 0.3

    diff_area = abs(area1 - area2)
    diff_compactness = abs(compactness1 - compactness2)
    diff_aspect_ratio = abs(aspect_ratio1 - 1)

    # Общая разница между домами с учетом весов
    total_diff = (weight_area * diff_area + weight_compactness * diff_compactness + weight_aspect_ratio * diff_aspect_ratio)

    # Нормализуем разницу по сумме весов
    total_weight = weight_area + weight_compactness + weight_aspect_ratio
    similarity = total_diff / total_weight

    return similarity


def load_polygon_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Extracting the first polygon's coordinates
    base_object = data[0]["ehitis"]["ehitiseKujud"]["ruumikuju"][0]
    return base_object["geometry"]["coordinates"][0]


building_ids = [
    "101010836", "101011193", "101013480",  # Kärberi
    "114012183", "114012184", "114012196",  # Tartu mnt
    "120530679", "120530734", "120530759",  # Meeliku
    "120643546", "120643547", "120643548",  # Pallasti
]

matrix = [["x"]]
for building_id in building_ids:
    matrix[0].append(building_id)

for index, building_id in enumerate(building_ids):
    matrix.append([building_id])

    for building_id2 in building_ids:
        house1 = load_polygon_from_json(f"{building_id}.ehr.json")
        house2 = load_polygon_from_json(f"{building_id2}.ehr.json")
        comparison = compare_houses(house1, house2)
        matrix[index + 1].append(comparison)

filename = "house_comparison.json"
with open(filename, 'w') as file:
    json.dump(matrix, file, indent=4)
