import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime

# 读取ERA5文件数据
era5_data = xr.open_dataset(
    r"D:\Study\Yunnan Uni\Atmos Physical\data\Ver 1.0\data2008_1.nc"
)

# 定义相关常数
P0 = 85000  # 参考压强（Pa）
Rd = 287  # 干空气的特定气体常数J/(Kg·K)
Cp = 1004  # 干空气等压比热容J/(Kg·K)

# 定义区域范围
lon_range = [100, 110]
lat_range = [22, 30]

# 读取中国各省边界数据
china_provinces = gpd.read_file(
    r"D:\Study\SHP\ChinaAdminDivisonSHP-master\2. Province\province.shp"
)

# 创建文件夹保存图片
import os

output_folder = "output_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# 创建画图函数
def plot_frame(i):
    # 选择时间点
    time_to_plot = era5_data.time[i].values
    data_at_time = era5_data.sel(time=time_to_plot)

    # 截取指定区域的数据
    regional_data = data_at_time.where(
        (data_at_time.latitude >= lat_range[0])
        & (data_at_time.latitude <= lat_range[1])
        & (data_at_time.longitude >= lon_range[0])
        & (data_at_time.longitude <= lon_range[1]),
        drop=True,
    )

    # 计算850hPa位温
    # 假设海拔影响不大，表面压强相当于850hPa
    T_kelvin = regional_data["t2m"]  # T已经是开尔文
    sp = regional_data["sp"]
    theta = T_kelvin * (P0 / sp) ** (Rd / Cp)

    # 绘图
    fig, ax = plt.subplots(figsize=(10, 10))
    theta.plot(ax=ax, x="longitude", y="latitude", cmap="viridis")  # 使用适当的色彩映射
    china_provinces.plot(ax=ax, color="none", edgecolor="gray")

    # 设置标题
    ax.set_title(f"850hPa Equivalent Potential Temperature\n{time_to_plot}")

    # 保存图像
    output_file = os.path.join(output_folder, f"frame_{i:04d}.png")
    plt.savefig(output_file)
    plt.close()


# 生成所有图片
for i in range(len(era5_data.time)):
    plot_frame(i)
