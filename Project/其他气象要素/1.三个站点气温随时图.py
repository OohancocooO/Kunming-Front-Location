# coding:utf-8
# coding:utf-8
import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False    # 解决保存图像是负号'-'显示为方块的问题

era5_data = xr.open_dataset(r"../../Dataset/data2008_1.nc")

# 昆明站,贵阳站，会泽站的经纬度
lon_3 = [102.73, 106.63, 103.32]
lat_3 = [25.04, 26.65, 26.41]
station = ["昆明站","贵阳站","会泽站"]

# 创建一个空字典来存储站点数据
station_data = {}

# 计算所给数据中最接近这三个站经纬度的数据点，得到lon和lat都只有一个维度，温度值与时间有关的数据
for i in range(3):
    lon_diff = era5_data.longitude - lon_3[i]
    lat_diff = era5_data.latitude - lat_3[i]
    distances = np.sqrt(lon_diff ** 2 + lat_diff ** 2)
    distances_np = distances.values

    # 找到距离最小的格点的索引
    min_idx = np.unravel_index(np.argmin(distances_np, axis=None), distances_np.shape)

    # 提取距离最近的格点数据并存储到字典中
    station_data[f"data_at_station_{i + 1}"] = era5_data.isel(latitude=min_idx[0], longitude=min_idx[1])

fig, ax = plt.subplots(figsize=(10, 6))
len_x = None
# 遍历每个站点的数据，绘制温度随时间变化的折线图
for i in range(3):
    temperature = station_data[f"data_at_station_{i + 1}"].t2m
    t = temperature.sel(time=slice('2008-01-10T00:00:00.000000000', '2008-01-31T00:00:00.000000000', 24))
    # 将温度从开尔文转换为摄氏度
    t_celsius = t - 273.15
    len_x = len(t_celsius)
    ax.plot(range(len_x), t_celsius, label=station[i])


time_range = [f'2008-01-{i+10:02d}' for i in range(len_x)]
ax.set_xticks(range(0,len_x,3),time_range[::3],rotation = 20)
# 添加图例
ax.legend()
# 设置标题和轴标签
ax.set_title("Temperature Over Time for 3 Stations")
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (Celsius)")

# 显示图形
plt.show()
