import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# 读取中国各省边界数据
china_provinces = gpd.read_file(
    r"D:\Study\SHP\ChinaAdminDivisonSHP-master\2. Province\province.shp"
)

# 读取nc文件数据
data = xr.open_dataset(r"D:\Study\Yunnan Uni\Atmos Physical\data\data2008_1.nc")

sp = data["sp"]
t2m = data["t2m"]
u10 = data["u10"]

# 计算假相当位温
theta_e = (
    data["t2m"]
    * (1000 / sp) ** 0.286
    * np.exp((3.376 / (data["t2m"] + 273.15) - 0.00254) * (data["d2m"] - data["t2m"]))
)

# 提取经度和纬度
lon = data.longitude
lat = data.latitude

# 提取最接近1月10日13时的相当位温数据
theta_e_1_10_13 = theta_e.sel(time="2008-01-10T13:00:00", method="nearest")

# 创建相当位温分布图
fig, ax = plt.subplots(figsize=(10, 6))

# 设置经度和纬度的范围
lon_range = [100, 110]  # 经度范围
lat_range = [20, 30]  # 纬度范围
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)

# 生成每5个单位数值的等值线数值范围
levels = np.arange(theta_e_1_10_13.min(), theta_e_1_10_13.max(), 3)

contour_plot = theta_e_1_10_13.plot.contour(
    ax=ax, x="longitude", y="latitude", levels=levels, linewidths=1.4, cmap='rainbow'
)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Equivalent Potential Temperature on January 10, 13:00")

# 标注等值线上的数值
plt.clabel(contour_plot, inline=True, fontsize=8)

# 添加中国各省的边界
china_provinces.plot(ax=ax, color="none", edgecolor="gray")

# 创建颜色条
cbar = plt.colorbar(contour_plot, ax=ax)
cbar.set_label("Equivalent Potential Temperature (K)")

plt.show()
