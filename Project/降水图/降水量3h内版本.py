import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

# 读取ERA5文件数据
era5_data = xr.open_dataset("../../Dataset/data2008_1.nc")

# 选择日期
date_to_plot = "2008-01-12"
time_to_plot = "05:00:00"  # 选择特定时间点

# 选择该时间点的前一个小时和下一个小时
time_prev_hour = np.datetime64(date_to_plot + "T" + time_to_plot) - np.timedelta64(1, 'h')
time_next_hour = np.datetime64(date_to_plot + "T" + time_to_plot) + np.timedelta64(1, 'h')

# 选择数据
data_at_time_prev_hour = era5_data.sel(time=time_prev_hour)
data_at_time_next_hour = era5_data.sel(time=time_next_hour)

# 合并前一个小时和下一个小时的降水量数据
precipitation_combined = (data_at_time_prev_hour["tp"] + data_at_time_next_hour["tp"]) * 1000  # 将单位从米转换为毫米

# 定义区域范围
lon_range = [100, 110]
lat_range = [22, 30]

# 截取指定区域的数据
regional_data = precipitation_combined.where(
    (precipitation_combined.latitude >= lat_range[0])
    & (precipitation_combined.latitude <= lat_range[1])
    & (precipitation_combined.longitude >= lon_range[0])
    & (precipitation_combined.longitude <= lon_range[1]),
    drop=True,
)

# 将降水量为0的值设置为NaN
regional_data = regional_data.where(regional_data != 0)

# 定义颜色
colors = ["#FFFFFF","#A5F38D", "#39AA00", "#63BAFF", "#0000FE", "#FF00FF", "#810040"]
levels = [0, 0.5, 10, 25, 50, 100, 250, 400]
cmap = ListedColormap(colors)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

# 读取中国各省边界数据
china_provinces = gpd.read_file("../../Province_SHP/province.shp")

# 绘图
fig, ax = plt.subplots(figsize=(10, 10))

# 转换数据以适应 imshow()，这里假定regional_data仍有空间维度
regional_data_array = regional_data.values.squeeze()  # 移除多余的维度
# 获取坐标信息
lon = regional_data.longitude.values
lat = regional_data.latitude.values
# 计算地图绘制区域的范围
extent = [lon.min(), lon.max(), lat.min(), lat.max()]

# 绘制平滑图像
img = ax.imshow(
    regional_data_array,
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
ax.set_title(f"Combined 2-Hour Accumulated Precipitation (mm)\n{date_to_plot} {time_to_plot}")

# 显示图形
plt.show()
