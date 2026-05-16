import pandas as pd

# Lay danh sach 2000 short_p_id chinh xac tu gym_demo
demo = pd.read_csv('data_analysis/mvp_gym_demo.csv', usecols=['short_p_id'])
sampled_ids = set(demo['short_p_id'].tolist())
print(f'So nguoi mau: {len(sampled_ids)}')

# Doc weather theo chunk va loc xuong dung 2000 nguoi
print('Dang loc mvp_weather_behavior.csv (164MB)...')
chunks = pd.read_csv('data_analysis/mvp_weather_behavior.csv', chunksize=200000)
result_parts = []
for chunk in chunks:
    matched = chunk[chunk['short_p_id'].isin(sampled_ids)]
    result_parts.append(matched)

filtered = pd.concat(result_parts, ignore_index=True)
n_persons = filtered['short_p_id'].nunique()
print(f'So dong sau loc: {len(filtered):,}')
print(f'So nguoi doc nhat: {n_persons}')

filtered.to_csv('data_analysis/mvp_weather_behavior.csv', index=False)
print('Da luu lai mvp_weather_behavior.csv thanh cong!')
