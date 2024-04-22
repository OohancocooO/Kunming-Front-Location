import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime

# 读取ERA5文件数据
era5_data = xr.open_dataset("../../Dataset/data2008_1.nc")

# 选择时间点
time_to_plot = "2008-01-12T08:00:00"
data_at_time = era5_data.sel(time=time_to_plot)

# 定义相关常数
P0 = 85000  # 参考压强（Pa）
Rd = 287  # 干空气的特定气体常数J/(Kg·K)
Cp = 1004  # 干空气等压比热容J/(Kg·K)

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
china_provinces = gpd.read_file("../../Province_SHP/province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))
theta.plot(ax=ax, x="longitude", y="latitude", cmap="viridis")  # 使用适当的色彩映射
china_provinces.plot(ax=ax, color="none", edgecolor="gray")

# 设置标题
ax.set_title(f"850hPa Equivalent Potential Temperature\n{time_to_plot}")

# 显示图形
plt.show()
