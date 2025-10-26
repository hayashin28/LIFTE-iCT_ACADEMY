import random


time_map = {hour: round(random.uniform(7.8, 14.8), 1) for hour in range(8, 18)}

for hour, value in time_map.items():
    print(f"{hour}時 - {value}度")