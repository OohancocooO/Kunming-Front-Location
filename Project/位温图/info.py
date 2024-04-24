# nc文件的信息

import xarray as xr
import matplotlib.pyplot as plt

# 读取nc文件
dataset = xr.open_dataset("../../Dataset/data2008_1.nc")

# 接下来两行的路径也是正确的用法,相对路径也是可以的
# (r"d:\data\测试\uv300.nc")
# ('d:\\data\\测试\\uv300.nc')
# ('/mnt/d/data/ncl/uv300.nc')
# sp surface presure 地表气压
# tp Total precipitation 总降水量

# 找到变量名称
# var_name = "U"
t = dataset.d2m

# print(dataset)
print(dataset)
