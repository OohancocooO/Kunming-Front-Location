import imageio

# 指定图片所在的目录
image_directory = "./"
# 输出GIF的名称
output_gif = "output1.gif"

# 创建一个空列表来存储读入的图像
images = []

# 循环遍历所有的帧，从264到359
for i in range(264, 288):
    # 生成每一帧的文件名
    filename = f"../Atmos Physical/data/2008_01_map/{image_directory}frame_{i:04d}.png"
    # 读取图片并添加到列表中
    images.append(imageio.imread(filename))

# 通过读入的图片列表创建GIF
imageio.mimsave(
    output_gif, images, duration=0.1, loop=0
)  # 可以调整duration来设置每帧的显示时间


print("GIF已成功创建。")
