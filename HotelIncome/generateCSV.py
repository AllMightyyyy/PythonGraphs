import numpy as np
import pandas as pd

# Generate random data similar to file 1
regions = ['Norte', 'Sur', 'Este', 'Oeste']
room_types = ['Estandar', 'Deluxe', 'Suite']
years = ['2018', '2019', '2020', '2021', '2022']

hotel_data = []
for region in regions:
    for room in room_types:
        row = [region, room] + list(np.random.randint(20000, 120000, size=len(years)))
        hotel_data.append(row)

hotel_df = pd.DataFrame(hotel_data, columns=['Region', 'Habitacion'] + years)
hotel_df.to_csv('simulated_hotel_income.csv', index=False)
