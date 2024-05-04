row_2 = [1, 0.876, 0.686, 1, 0, 1, 1]
row_3 = [0.985, 0, 0.125, 0.319, 0.889, 0.364, 0.333]
row_4 = [0, 1, 1, 0.809, 0.111, 1, 0.444]
row_5 = [0.017, 0, 0, 0, 1, 0, 0]


def euclidian_distance(first, second):
    distance = 0.0
    for index in range(len(first)):
        distance += (first[index] - second[index]) ** 2
    return round(distance ** 0.5, 4)


distances = [
    euclidian_distance(row_2, row_3),
    euclidian_distance(row_2, row_4),
    euclidian_distance(row_2, row_5),
    euclidian_distance(row_3, row_4),
    euclidian_distance(row_3, row_5),
    euclidian_distance(row_4, row_5)
]

print(distances)
print()
print(f"Minimum distance: {min(distances)}")
print(f"Maximum distance: {max(distances)}")
print()


row_6 = [1, 0, 0, 0.617, 0.278, 1, 0]
new_distances = [
    euclidian_distance(row_6, row_2),
    euclidian_distance(row_6, row_3),
    euclidian_distance(row_6, row_4),
    euclidian_distance(row_6, row_5)
]

print(new_distances)
print()
print(f"Minimum distance: {min(new_distances)}")
print(f"Maximum distance: {max(new_distances)}")
