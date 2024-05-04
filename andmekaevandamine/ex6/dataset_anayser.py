import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_histogram(data, column, title):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, color='blue', bins=30)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()


columns = [
    '% clientele female', '% clientele local', '% clientele U.S.A.', '% clientele South America',
    '% clientele Europe', '% clientele M.East Africa', '% clientele Asia', '% businessmen', '% tourists',
    '% direct reservations', '% agency reservations', '% air crews', '% clients under 20 years',
    '% clients 20-35 years', '% clients 35-55 years', '% clients more than 55 yrs', 'price of rooms',
    'length of stay', '% occupancy'
]
data = pd.read_excel('Bertin_s_hotel_example.xls')
data = data.transpose()
data.columns = columns
data = data.drop(data.index[0])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# print(data)

data['avg_client_age'] = (
    data['% clients under 20 years'] * 15 +
    data['% clients 20-35 years'] * 27.5 +
    data['% clients 35-55 years'] * 45 +
    data['% clients more than 55 yrs'] * 65
) / 100

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(data['price of rooms'], data['avg_client_age'], color='blue', alpha=0.7)
plt.title('Correlation between Price of Rooms and Client Age (Figure 2)')
plt.xlabel('Price of Rooms')
plt.ylabel('Average Age of Clients')
plt.grid(True)
plt.show()

# plt.scatter(data['% businessmen'], data['% tourists'], c=data['length of stay'], cmap='viridis')
# plt.colorbar(label='length of stay')
# plt.xlabel('businessmen %')
# plt.ylabel('tourists %')
# plt.title('Correlation between clients type and length of stay (Figure 3)')
# plt.show()
