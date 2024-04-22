# coding:utf-8
import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt

era5_data = xr.open_dataset(r"../../Dataset/data2008_1.nc")

# 选择时间点
time_to_plot = "2008-01-12T08:00:00"
data_at_time = era5_data.sel(time=time_to_plot)

# 定义相关常数,不想在风场里画等位温先了，暂时不算位温
# P0 = 100000  # 参考压强（Pa）
# Rd = 287  # 干空气的特定气体常数J/(Kg·K)
# Cp = 1004  # 干空气等压比热容J/(Kg·K)

# 提取u10和v10数据并进行约束到指定的经纬度范围
# u10_data = era5_data["u10"]
# v10_data = era5_data["v10"]

# 获取经度和纬度坐标
# lons = u10_data.longitude.values
# lats = u10_data.latitude.values

# 定义区域范围,云南的经纬度大致范围
lon_range = [100, 110]
lat_range = [22, 30]

# 截取指定区域的数据
rd = data_at_time.where(
    (data_at_time.latitude >= lat_range[0])
    & (data_at_time.latitude <= lat_range[1])
    & (data_at_time.longitude >= lon_range[0])
    & (data_at_time.longitude <= lon_range[1]),
    drop=True,
)



# 绘制风向图
fig, ax = plt.subplots(figsize=(10, 10),dpi=300)

# 绘制风向箭头
step = 5
# 绘制风向箭头
ax.quiver(
    rd.longitude[::step],
    rd.latitude[::step],
    rd.u10[::step, ::step],
    rd.v10[::step, ::step],
    scale=100,
)

# 添加中国各省的边界
china_provinces = gpd.read_file("../../Province_SHP/province.shp")
china_provinces.plot(ax=ax, color="none", edgecolor="#006699")


# 设置绘图范围以限制SHP文件在指定区域内显示
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)

# 设置标题和轴标签
ax.set_title(f"Wind Direction\n{time_to_plot}")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# 显示图形
plt.show()
