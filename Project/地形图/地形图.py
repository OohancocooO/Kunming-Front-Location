# 由于文件过大没上传，所以运行不出来
# 由于文件过大没上传，所以运行不出来
# 由于文件过大没上传，所以运行不出来

import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd
import os
import numpy as np

# 定义文件夹路径和省界shapefile的路径
folder_path = "path/to/your/tiff/files"
province_shp_path = "path/to/province.shp"

# 读取文件夹中的所有tif文件
file_list = [
    os.path.join(folder_path, f"ALPSMLC30_N0{a}E{b}_DSM.tif")
    for a in range(22, 30)
    for b in range(100, 110)
]

# 将tif文件合并为一个单独的栅格数据集
src_files_to_mosaic = []
for fp in file_list:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)
mosaic, out_trans = merge(src_files_to_mosaic)

# 读取合并后的数据和转换参数
raster = mosaic[0]  # 假设海拔数据在第一波段

# 获取地理坐标范围（左下角和右上角的经纬度）
transform = out_trans
west, north = transform * (0, 0)
east, south = transform * (raster.shape[1], raster.shape[0])

# 创建地形图的分层设色
elevation_min = np.min(raster)
elevation_max = np.max(raster)
colormap = LinearSegmentedColormap.from_list(
    "elevation", ["green", "yellow", "brown", "gray", "white"]
)

# 读取省界shapefile
province_boundaries = gpd.read_file(province_shp_path)

# 裁剪省界数据，只保留指定经纬度范围内的部分
extent = (100, 110, 22, 30)  # 东经100到110，北纬22到30
province_boundaries = province_boundaries.cx[
    extent[0] : extent[1], extent[2] : extent[3]
]

# 设置地图和省界的绘制属性
fig, ax = plt.subplots(figsize=(10, 10))
raster_img = ax.imshow(
    raster,
    cmap=colormap,
    extent=(west, east, south, north),
    vmin=elevation_min,
    vmax=elevation_max,
)
province_boundaries.boundary.plot(ax=ax, edgecolor="black")

# 设置坐标轴的标签和范围
ax.set_title("Elevation and Province Boundaries")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_xlim(100, 110)
ax.set_ylim(22, 30)

# 添加图例
cbar = fig.colorbar(raster_img, ax=ax)
cbar.set_label("Elevation (m)")

# 展示地图
plt.show()
