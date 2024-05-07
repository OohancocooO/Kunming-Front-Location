import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature


# 定义计算相当位温的函数
def calculate_theta_e(T, Td, P):
    R_d = 287.05
    C_pd = 1004
    e_s = 6.112 * np.exp((17.67 * (T - 273.15)) / (T - 29.65))
    a = 7.5
    b = 237.3
    e = e_s * np.exp(a * (Td - 273.15) / (Td - b)) / np.exp(a * (T - 273.15) / (T - b))
    x = 0.622 * e / (P - e)
    T_LCL = 1 / (1 / (Td - 56) + np.log(T / Td) / 800) + 56
    theta_e = (
        T
        * (1000 / (P - e)) ** (R_d / C_pd)
        * (T / T_LCL) ** (0.28 * x)
        * np.exp(((3036.0 / T_LCL) - 1.78) * x * (1 + 0.448 * x))
    )
    return theta_e


# 读取shp文件并限定范围
gdf = gpd.read_file("../../Province_SHP/province.shp")
gdf = gdf.cx[100:110, 22:30]  # 限定在北纬22-30，东经100-110之间


# 读取.nc文件
ds = xr.open_dataset("../../Dataset/data2008_1.nc")
# 选择时间点
time_to_plot = "2008-01-12T08:00:00"
data_at_time = ds.sel(time=time_to_plot)
t2m = ds["t2m"]  # 地表温度
d2m = ds["d2m"]  # 露点温度
sp = ds["sp"] / 100  # 地表气压转换为hPa

# 计算相当位温
theta_e = calculate_theta_e(t2m, d2m, sp)

# 绘图
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
# 因相当位温θe计算可能涉及整个时间序列，这里取均值绘图时需确保时间维度存在且正确处理
mean_theta_e = theta_e.mean(dim="time")
mean_theta_e.plot(
    ax=ax,
    x="longitude",
    y="latitude",
    cmap="coolwarm",
    add_colorbar=True,
    extend="neither",
)

# 添加300K等值线
# 注意: contour函数需要显式传入经纬度网格，确保theta_e是具有正确维度（时间除外）的xarray.DataArray
CS = plt.contour(
    mean_theta_e.longitude,
    mean_theta_e.latitude,
    mean_theta_e,
    levels=[300],
    colors="k",
    linewidths=2,
    transform=ccrs.PlateCarree(),
)
# plt.clabel(
#    CS, inline=True, fontsize=10, fmt="%1.0fK"
# )  # 可选：为等值线添加文本标签，例如温度标签

# 添加shp文件图层
gdf.plot(ax=ax, facecolor="none", edgecolor="gray")

# 限定地图范围
ax.set_extent([100, 110, 22, 30])

# 设置标题和轴标签
ax.set_title(f"850hPa Equivalent potential temperature Contour\n{time_to_plot}")
# 添加网格线（经纬度线）和标签
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False  # 关闭顶部标签
gl.right_labels = False  # 关闭右侧标签
gl.xformatter = LONGITUDE_FORMATTER  # 设置经度标签格式
gl.yformatter = LATITUDE_FORMATTER  # 设置纬度标签格式
gl.xlabel_style = {'size': 12, 'color': 'black'}  # 设置纬度标签样式
gl.ylabel_style = {'size': 12, 'color': 'black'}  # 设置经度标签样式


plt.show()
