import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime

# 读取ERA5文件数据
era5_data = xr.open_dataset("Dataset\\data2008_1.nc")

# 选择时间点
time_to_plot = "2008-01-12T08:00:00"
data_at_time = era5_data.sel(time=time_to_plot)

# 定义相关常数
P0 = 100000  # 参考压强（Pa）
Rd = 287  # 干空气的特定气体常数J/(Kg·K)
Cp = 1004  # 干空气等压比热容J/(Kg·K)

# 提取u10和v10数据并进行约束到指定的经纬度范围
u10_data = era5_data["u10"]
v10_data = era5_data["v10"]

# 获取经度和纬度坐标
lons = u10_data.longitude.values
lats = u10_data.latitude.values

# 定义区域范围
lon_range = [100, 110]
lat_range = [22, 30]

# 截取指定区域的数据
regional_data = data_at_time.where(
    (data_at_time.latitude >= lat_range[0])
    & (data_at_time.latitude <= lat_range[1])
    & (data_at_time.longitude >= lon_range[0])
    & (data_at_time.longitude <= lon_range[1]),
    drop=True,
)

# 计算相对湿度
Td = regional_data["d2m"] - 273.15  # 摄氏度
T = regional_data["t2m"] - 273.15  # 摄氏度
RH = np.exp((17.27 * Td) / (243.04 + Td)) / np.exp((17.27 * T) / (243.04 + T)) * 100

# 计算850hPa位温
# 假设海拔影响不大，表面压强相当于850hPa
T_kelvin = regional_data["t2m"]  # T已经是开尔文
sp = regional_data["sp"]
theta = T_kelvin * (P0 / sp) ** (Rd / Cp)

# 读取中国各省边界数据
china_provinces = gpd.read_file("Province_SHP\\province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))

# 绘制等值线
lon, lat = np.meshgrid(regional_data.longitude, regional_data.latitude)
# theta = regional_data["t2m"]  # 示例中为了简化，我们直接使用t2m表示
contours = ax.contour(lon, lat, theta.squeeze(), levels=20, colors='#666666')
ax.clabel(contours, inline=True, fontsize=8)

# 使用contourf填充u10和v10同时大于0的部分
u10_greater_than_0 = regional_data["u10"].where(
    (regional_data["u10"] > 0) & (regional_data["v10"] > 0)
)
lon_greater_than_0, lat_greater_than_0 = np.meshgrid(
    u10_greater_than_0.longitude, u10_greater_than_0.latitude
)
ax.contourf(
    lon_greater_than_0,
    lat_greater_than_0,
    u10_greater_than_0.squeeze(),
    colors="#FFFFCC",
)

# 使用contourf填充u10和v10同时小于0的部分
u10_less_than_0 = regional_data["u10"].where(
    (regional_data["u10"] < 0) & (regional_data["v10"] < 0)
)
lon_less_than_0, lat_less_than_0 = np.meshgrid(
    u10_less_than_0.longitude, u10_less_than_0.latitude
)
ax.contourf(
    lon_less_than_0, lat_less_than_0, u10_less_than_0.squeeze(), colors="#FFCCCC"
)

# 添加中国各省的边界
china_provinces.plot(ax=ax, color="none", edgecolor="#006699")

# 设置绘图范围以限制SHP文件在指定区域内显示
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)

# 设置标题和轴标签
ax.set_title(f"850hPa Equivalent Potential Temperature Contour\n{time_to_plot}")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# 显示图形
plt.show()
