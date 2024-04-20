import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# 载入数据
data_file = r"D:\Study\Yunnan Uni\Atmos Physical\data\data2008_1.nc"
ds = xr.open_dataset(data_file)

# 读取中国各省边界数据
china_provinces = gpd.read_file(
    r"D:\Study\SHP\ChinaAdminDivisonSHP-master\2. Province\province.shp"
)

# 常量
R_d = 307.05
c_pd = 1004.7
kappa = R_d / c_pd  # Rd/cpd


# 函数计算位温
def calculate_potential_temperature(t2m, sp):
    return t2m * (1000 / sp) ** kappa


# 函数计算梯度的大小
def calculate_gradient_magnitude(da, delta_lon=5, delta_lat=5):
    grad_x = da.diff("longitude", delta_lon)
    grad_y = da.diff("latitude", delta_lat)
    return np.sqrt(grad_x**2 + grad_y**2)


# 使用 ERA5 数据
sp = ds["sp"]
t2m = ds["t2m"]
u10 = ds["u10"]


# 计算梯度大小
grad_theta = calculate_gradient_magnitude(
    theta_interp, delta_lon=50, delta_lat=50
).fillna(
    0
)  # 50代表距离网格点的距离

# 转换为 Numpy 数组
grad_theta_numpy = grad_theta.values

# 阈值
threshold = 8 / 110

# 找到30N最近的纬度索引
lat_30_index = np.argmin(np.abs(new_lat - 30))

# 创建相当位温分布图
fig, ax = plt.subplots(figsize=(10, 6))

theta_e = calculate_potential_temperature(t2m, sp)

# 提取最接近1月10日13时的相当位温数据
theta_e_1_10_13 = theta_e.sel(time="2008-01-10T13:00:00", method="nearest")

# 设置经度和纬度的范围
lon_range = [100, 110]  # 经度范围
lat_range = [20, 30]  # 纬度范围
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)

# 生成每5个单位数值的等值线数值范围
levels = np.arange(theta_e_1_10_13.min(), theta_e_1_10_13.max(), 3)

contour_plot = theta_e_1_10_13.plot.contour(
    ax=ax, x="longitude", y="latitude", levels=levels, linewidths=1.4, cmap="rainbow"
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
