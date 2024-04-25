# 由于文件过大没上传，所以运行不出来
# 由于文件过大没上传，所以运行不出来
# 由于文件过大没上传，所以运行不出来

import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# 昆明和贵阳的经纬度
kunming_coords = (102.8332, 24.8797)
guiyang_coords = (106.6302, 26.6476)


# 计算两点间直线的函数
def interpolate_line(start, end, num=100):
    """在两点之间插值直线，num定义插值点数"""
    x = np.linspace(start[0], end[0], num=num)
    y = np.linspace(start[1], end[1], num=num)
    return x, y


# 插值直线上的点
line_xs, line_ys = interpolate_line(kunming_coords, guiyang_coords)

# 准备读取tif文件并提取海拔数据
elevations = []
for a in range(22, 30):  # 纬度范围
    for b in range(100, 110):  # 经度范围
        filename = f"ALPSMLC30_N0{a}E{b}_DSM.tif"
        try:
            with rasterio.open(filename) as src:
                for x, y in zip(line_xs, line_ys):
                    # 首先检查坐标是否落在当前文件范围内
                    if (
                        x < src.bounds.left
                        or x > src.bounds.right
                        or y < src.bounds.bottom
                        or y > src.bounds.top
                    ):
                        # 坐标不在当前tif文件的范围内
                        continue

                    # 注意：这里将x和y的使用顺序调整为先经度x（东经），后纬度y（北纬）
                    row, col = src.index(x, y)

                    # 安全地检查行列索引是否在数组边界内
                    if (row >= 0 and row < src.height) and (
                        col >= 0 and col < src.width
                    ):
                        value = src.read(1)[row, col]
                        elevations.append(value)
                    else:
                        # 索引超出范围时的处理（可选择跳过或用特定值标记）
                        elevations.append(np.nan)
        except FileNotFoundError:
            print(f"{filename} not found.")
            continue

# 使用线性插值填充海拔数据中的NaN值
elevations = np.array(elevations)
valid_elevations = elevations[~np.isnan(elevations)]
valid_points = np.arange(len(elevations))[~np.isnan(elevations)]
interpolator = interp1d(valid_points, valid_elevations, fill_value="extrapolate")
elevations = interpolator(np.arange(len(elevations)))

# 绘制海拔剖面图
plt.figure(figsize=(10, 6))
plt.plot(elevations, label="Elevation Profile")
plt.xlabel("Distance")
plt.xticks([0, len(elevations) - 1], ["Kunming", "Guiyang"])
plt.ylabel("Elevation (m)")
plt.title("Elevation Profile from Kunming to Guiyang")
plt.legend()
plt.show()
