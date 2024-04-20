import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import geopandas as gpd
import pandas as pd
from matplotlib.colors import Normalize

from matplotlib.font_manager import FontProperties

# 设置Matplotlib的默认字体
plt.rcParams["font.sans-serif"] = ["cjkFonts ???"]  # 指定默认字体为微软雅黑
plt.rcParams["axes.unicode_minus"] = False  # 正确显示负号


# 计算相对湿度的函数
def calculate_relative_humidity(Td, T):
    return np.exp(17.27 * Td / (243.04 + Td)) / np.exp(17.27 * T / (243.04 + T)) * 100


# 计算位温的函数
def calculate_potential_temperature(T, P):
    P0 = 1000  # hPa
    Rd = 287  # J/(kg·K)
    Cp = 1004  # J/(kg·K)
    # 计算混合比q，这里简化处理，不考虑q对R的调整，因为没有提供水汽压等信息
    R = Rd * (1 + 0.61 * 0)  # 假设混合比q=0
    return T * (P0 / P) ** (R / Cp)


# 读取数据
data = xr.open_dataset(r"D:\Study\Yunnan Uni\Atmos Physical\data\Ver 1.0\data2008_1.nc")

# 新增选择指定时间和气压层的步骤
time = "2008-01-12T14:00:00"
pressure_level = 850

# 使用.sel()方法来选择特定的时间和气压层
selected_data = data.sel(time=time, level=pressure_level, method="nearest")

# 读取中国各省边界数据
china_provinces = gpd.read_file(
    r"D:\Study\SHP\ChinaAdminDivisonSHP-master\2. Province\province.shp"
)
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})


# 设置经纬度范围
lon_range = [100, 110]
lat_range = [20, 30]
ax.set_xlim(lon_range)
ax.set_ylim(lat_range)


# 绘图的辅助函数
def draw_frame(time_step):
    ax.clear()
    # 设置地图的背景色
    ax.background_img.set_visible(False)
    ax.outline_patch.set_visible(False)

    # 绘制基本地图
    china_provinces.plot(ax=ax, color="none", edgecolor="black")

    # 调用计算相对湿度和位温的函数
    T = data.t2m.sel(time=time_step)  # 2m气温
    Td = data.d2m.sel(time=time_step)  # 露点温度
    P = data.sp.sel(time=time_step)  # 表面气压

    RH = calculate_relative_humidity(Td - 273.15, T - 273.15)
    θ = calculate_potential_temperature(T, P / 100)

    # 绘制位温图
    # 使用Normalize确保数据级间距均匀
    norm = Normalize(vmin=250, vmax=310)
    img = ax.contourf(
        data.longitude,
        data.latitude,
        θ,
        levels=np.linspace(250, 310, 61),
        cmap="RdYlBu_r",
        norm=norm,
    )

    # 添加色带
    plt.colorbar(img, ax=ax, label="Potential Temperature (K)")

    # 正确使用了pandas进行时间格式的转换和格式化
    ax.set_title(pd.to_datetime(str(time_step)).strftime("%Y-%m-%d %H:%M:%S"))

    return (img,)


plt.title("850hPa Equivalent Potential Temperature - 2008-01-12 14:00:00 UTC")

# 绘制特定时间和气压层的图
draw_frame()

plt.show()
