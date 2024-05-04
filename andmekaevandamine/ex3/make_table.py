import json
from tabulate import tabulate


with open("house_comparison.json", 'r') as file:
    data = json.load(file)
    print(tabulate(data, headers="firstrow", tablefmt="plain"))


# with open('result.txt', 'r') as file:
#     lines = file.readlines()
#
# data = [line.strip().split(',') for line in lines]
# print(tabulate(data, headers="firstrow", tablefmt="plain"))
