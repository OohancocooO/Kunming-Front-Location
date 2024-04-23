import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt

# 读取ERA5文件数据
era5_data = xr.open_dataset("../../Dataset/data2008_1.nc")

# 选择日期
date_to_plot = "2008-01-01T"

# 选择该日期内的所有时间点
data_at_date = era5_data.sel(time=date_to_plot)

# 定义区域范围
lon_range = [100, 110]
lat_range = [22, 30]

# 截取指定区域的数据
regional_data = data_at_date.where(
    (data_at_date.latitude >= lat_range[0])
    & (data_at_date.latitude <= lat_range[1])
    & (data_at_date.longitude >= lon_range[0])
    & (data_at_date.longitude <= lon_range[1]),
    drop=True,
)

# 提取降水数据并将单位转换为毫米
precipitation = regional_data["tp"] * 1000  # 将单位从米转换为毫米

# 将时间维度合并为一维数组，并对降水量进行累积
accumulated_precipitation = precipitation.resample(time="24H").sum()

# 读取中国各省边界数据
china_provinces = gpd.read_file("../../Province_SHP/province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))
accumulated_precipitation.plot(ax=ax, x="longitude", y="latitude", cmap="Blues")  # 使用适当的色彩映射
china_provinces.plot(ax=ax, color="none", edgecolor="gray")

# 设置标题
ax.set_title(f"24-Hour Accumulated Precipitation (mm)\n{date_to_plot}")

# 显示图形
plt.show()

