import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# 读取ERA5文件数据
era5_data = xr.open_dataset("../../Dataset/data2008_1.nc")

# 选择日期
date_to_plot = "2008-01-12"

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
accumulated_precipitation = precipitation.resample(time="24h").sum()

# 将降水量为0的值设置为NaN ##这里好像有点问题（胡留）
accumulated_precipitation = accumulated_precipitation.where(
    accumulated_precipitation != 0
)

# 定义颜色
colors = ["#FFFFFF","#A5F38D", "#39AA00", "#63BAFF", "#0000FE", "#FF00FF", "#810040"]
levels = [0, 2, 10, 25, 50, 100, 250, 400]
cmap = ListedColormap(colors)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

# 读取中国各省边界数据
china_provinces = gpd.read_file("../../Province_SHP/province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))

# 转换数据以适应 imshow()，这里假定accumulated_precipitation仍有空间维度
accumulated_precip_array = accumulated_precipitation.values.squeeze()  # 移除多余的维度
# 获取坐标信息
lon = accumulated_precipitation.longitude.values
lat = accumulated_precipitation.latitude.values
# 计算地图绘制区域的范围
extent = [lon.min(), lon.max(), lat.min(), lat.max()]

# 绘制平滑图像
img = ax.imshow(
    accumulated_precip_array,
    extent=extent,
    origin="upper",
    cmap=cmap,
    norm=norm,
    interpolation="bilinear",
)

# 绘制省界
china_provinces.plot(ax=ax, color="none", edgecolor="gray")

# 调整地图显示范围
ax.set_xlim([lon_range[0], lon_range[1]])
ax.set_ylim([lat_range[0], lat_range[1]])

# 添加色标
cb = plt.colorbar(img, ax=ax, boundaries=levels, extend="max")
cb.set_label("Accumulated Precipitation (mm)")

# 设置标题
ax.set_title(f"24-Hour Accumulated Precipitation (mm)\n{date_to_plot}")

# 显示图形
plt.show()
