import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import geopandas as gpd
import cartopy.crs as ccrs


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
theta_e.mean(dim="time").plot(ax=ax, x="longitude", y="latitude", cmap="coolwarm")

# 添加shp文件图层
gdf.plot(ax=ax, facecolor="none", edgecolor="gray")

# 限定地图范围
ax.set_extent([100, 110, 22, 30])

# 设置标题和轴标签
ax.set_title(f"850hPa Equivalent potential temperature Contour\n{time_to_plot}")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
