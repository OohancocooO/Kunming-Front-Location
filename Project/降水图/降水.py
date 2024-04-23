import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt

# 读取ERA5文件数据
era5_data = xr.open_dataset("../../Dataset/data2008_1.nc")

# 选择时间点
time_to_plot = "2008-01-12T08:00:00"
data_at_time = era5_data.sel(time=time_to_plot)

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

# 提取降水数据并将单位转换为毫米
precipitation = regional_data["tp"] * 1000  # 将单位从米转换为毫米

# 读取中国各省边界数据
china_provinces = gpd.read_file("../../Province_SHP/province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))
precipitation.plot(ax=ax, x="longitude", y="latitude", cmap="Blues")  # 使用适当的色彩映射
china_provinces.plot(ax=ax, color="none", edgecolor="gray")

# 设置标题
ax.set_title(f"Precipitation (mm)\n{time_to_plot}")

# 显示图形
plt.show()
