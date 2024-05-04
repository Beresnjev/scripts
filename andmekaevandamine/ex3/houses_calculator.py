import numpy as np

houses = [
    784.0, 1984, 12401.0, 120, 5, 0, 927.0,
    593.1, 1984, 9473.0, 90, 5, 0, 680.8,
    782.1, 1984, 12526.0, 120, 5, 0, 914.9,
    322.6, 1968, 3215.0, 36, 3, 0, 0,
    372.3, 1968, 3289.0, 36, 3, 0, 257.3,
    398.1, 1973, 3817.0, 36, 3, 0, 302.6,
    577.6, 2008, 10369.3, 90, 5, 2, 269.5,
    573.9, 2008, 10267.3, 90, 5, 2, 634.4,
    574.0, 2008, 10267.3, 90, 5, 2, 634.4,
    389.9, 2014, 5502.0, 55, 5, 0, 179.1,
    390.2, 2013, 5502.0, 52, 5, 0, 179.1,
    384.9, 2013, 5502.0, 54, 5, 0, 179.1,
]

# Convert houses to a 2D numpy array
houses_array = np.array(houses).reshape(-1, 7)

# Normalize each column
min_values = houses_array.min(axis=0)
max_values = houses_array.max(axis=0)
normalized_houses = (houses_array - min_values) / (max_values - min_values)

print("Normalized Data:")
print(normalized_houses)
print()
print()

normalized_houses_list = normalized_houses.tolist()

print("Normalized Data (as Python list):")
print(normalized_houses_list)


def euclidian_distance(first, second):
    distance = 0.0
    for index in range(len(first)):
        distance += (first[index] - second[index]) ** 2
    return round(distance ** 0.5, 4)


num_rows = len(normalized_houses_list)
distance_matrix = [[0.0] * num_rows for _ in range(num_rows)]

# Calculate Euclidean distances between every row using every normalized parameter
for i in range(num_rows):
    for j in range(i+1, num_rows):
        dist = euclidian_distance(normalized_houses_list[i], normalized_houses_list[j])
        distance_matrix[i][j] = dist
        distance_matrix[j][i] = dist  # Distance matrix is symmetric

# Print the distance matrix
print("Distance Matrix:")
for row in distance_matrix:
    print(row)
