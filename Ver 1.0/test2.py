import numpy as np
import xarray as xr
import scipy.ndimage

# 载入数据
data_file = r"D:\Study\Yunnan Uni\Atmos Physical\data\data2012_01_p.nc"
ds = xr.open_dataset(data_file)

# 常量
R_d = 287.05
c_pd = 1004.7
kappa = R_d / c_pd  # Rd/cpd


# 函数计算位温
def calculate_potential_temperature(t2m, sp):
    return t2m * (1000 / sp) ** kappa


# 函数计算梯度的大小
def calculate_gradient_magnitude(da, delta_deg=5):
    grad_x = da.diff("longitude", delta_deg)
    grad_y = da.diff("latitude", delta_deg)
    return np.sqrt(grad_x**2 + grad_y**2)


# 使用 ERA5 数据
sp = ds["sp"]  # 表面气压
t2m = ds["t2m"]  # 2 米温度
u10 = ds["u10"]  # 10 米风
lons = ds["longitude"]
lats = ds["latitude"]
times = ds["time"]

# 计算位温
theta = calculate_potential_temperature(t2m, sp)

# 插值到格网
new_lon = np.arange(100, 110.1, 0.1)
new_lat = np.arange(30, 19.9, -0.1)
theta_interp = theta.interp(longitude=new_lon, latitude=new_lat)

# 计算梯度大小
grad_theta = calculate_gradient_magnitude(theta_interp)

# 转换为 Numpy 数组
grad_theta_numpy = grad_theta.values

# 阈值
threshold = 8 / 110

# 找出初选点
front_points = np.where(grad_theta_numpy >= threshold)

# 找 u10 的梯度值，并筛选出初选点
u10_interp = u10.interp(longitude=new_lon, latitude=new_lat)
delta_u = calculate_gradient_magnitude(u10_interp).values

# 设置条件初选和复选点
mask_front_points = delta_u[front_points] > 1

# 抽取复选点
front_points_filtered = np.array(front_points)[:, mask_front_points]

# 找到26N最近的纬度索引
lat_26_index = np.argmin(np.abs(new_lat - 26))

# 筛选26N的锋线位置
front_points_at_26N = front_points_filtered[:, front_points_filtered[1] == lat_26_index]

# 保存结果到文本文件
output_file = "front_position.txt"
with open(output_file, "w") as file:
    file.write("TIME\tLONGITUDE\n")
    for time_idx, lat_idx, lon_idx in front_points_at_26N.T:
        # 确认是否满足其他条件
        if delta_u[time_idx, lat_idx, lon_idx] > 1:
            # 写入26N纬度上的锋线位置
            time_formatted = str(times[time_idx].dt.strftime("%Y-%m-%d %H:%M:%S").data)
            file.write(f"{time_formatted}\t{new_lon[lon_idx]:.2f}\n")

# 打印保存信息
print(f"Front position result has been saved to {output_file}")
