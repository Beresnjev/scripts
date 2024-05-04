import pandas as pd
import math


def convert_xls(file_path):
    table = pd.read_excel(file_path)
    item_sets = []
    current_buyer = ""
    current_set = []
    for index, row in table.iterrows():
        if current_buyer == "" or current_buyer != row['ostja']:
            current_buyer = row['ostja']
            if current_set:
                item_sets.append(current_set)
            current_set = []

        element = row['kaup']
        element = element.replace(",", "")
        element_word = '_'.join(element.split(' '))
        current_set.append(element_word)

    return item_sets


def convert_csv(file_path):
    data = pd.read_csv(file_path)
    data.drop('id', axis=1, inplace=True)
    interval_columns = ['age', 'income']
    boolean_columns = ['married', 'children', 'car', 'save_act', 'current_act', 'mortgage', 'pep']

    for column in interval_columns:
        min_value = data[column].min()
        max_value = data[column].max()
        interval_length = (max_value - min_value) / 5
        data[column] = data[column].apply(lambda x: get_interval(column, min_value, interval_length, x))

    for column in boolean_columns:
        data[column] = data[column].apply(lambda x: f'{column}_{x}')

    return data.values.tolist()


def get_interval(column, min_value, interval_length, value):
    interval_number = math.ceil((value - min_value) / interval_length)
    interval_start = round(min_value + (interval_number - 1) * interval_length, 1)
    interval_end = round(min_value + interval_number * interval_length, 1)
    return f'{column}_{interval_start}_{interval_end}'


def write_data_to_input(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for item_set in data:
            file.write(' '.join(item_set) + '\n')


xls_filepath = './files/tshekid_office2003.xls'
sets = convert_xls(xls_filepath)
write_data_to_input(sets, './inputs/input1.txt')

csv_filepath = './files/bank-data.csv'
sets = convert_csv(csv_filepath)
write_data_to_input(sets, './inputs/input2.txt')
