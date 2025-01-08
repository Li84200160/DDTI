import cv2
import numpy as np
import os
import random
from PIL import Image


# 读取 mask 图像
def read_mask_image(mask_path):
    try:
        # 使用 OpenCV 读取 mask 图像，并转换为灰度图
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        return mask
    except Exception as e:
        print(f"Error reading mask image: {e}")
        return None


# 应用膨胀操作
def dilate_mask(mask, kernel_size=5, iterations=1):
    # 创建一个内核（结构元素），使用小矩形内核进行膨胀操作
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(mask, kernel, iterations=iterations)


# 应用腐蚀操作
def erode_mask(mask, kernel_size=5, iterations=1):
    # 创建一个内核（结构元素），使用小矩形内核进行腐蚀操作
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(mask, kernel, iterations=iterations)


# 随机旋转图像
def rotate_image(image, angle):
    # 使用 PIL 旋转图像
    pil_image = Image.fromarray(image)
    rotated_image = pil_image.rotate(angle, expand=True, fillcolor=0)
    return np.array(rotated_image)


# 保存处理后的 mask 图像
def save_mask_image(mask, output_path):
    try:
        # 将 numpy 数组转换为 PIL 图像
        mask_image = Image.fromarray(mask)
        mask_image.save(output_path)
        print(f"Saved processed mask image to {output_path}")
    except Exception as e:
        print(f"Error saving mask image: {e}")


# 随机选择并应用处理操作
def process_mask_randomly(mask_path, output_directory):
    mask = read_mask_image(mask_path)
    if mask is None:
        return

    # 随机选择操作类型
    operation = random.choice(['dilate', 'erode'])

    if operation == 'dilate':
        # 随机选择膨胀的内核大小和迭代次数
        kernel_size = random.choice([3, 5, 7])
        iterations = random.choice([1, 2, 3])
        print(f"Applying dilate operation with kernel size {kernel_size} and {iterations} iterations")
        processed_mask = dilate_mask(mask, kernel_size, iterations)

    elif operation == 'erode':
        # 随机选择腐蚀的内核大小和迭代次数
        kernel_size = random.choice([3, 5, 7])
        iterations = random.choice([1, 2, 3])
        print(f"Applying erode operation with kernel size {kernel_size} and {iterations} iterations")
        processed_mask = erode_mask(mask, kernel_size, iterations)

    # 随机选择旋转角度（±5度范围）
    angle = random.uniform(-5, 5)
    print(f"Applying rotation with angle {angle:.2f} degrees")
    processed_mask = rotate_image(processed_mask, angle)

    # 保存处理后的 mask 图像，使用原始文件名
    filename = os.path.basename(mask_path)  # 获取原始文件名
    output_path = os.path.join(output_directory, filename)
    save_mask_image(processed_mask, output_path)


# 处理文件夹中的所有 mask 图像
def process_masks_in_directory(input_directory, output_directory):
    # 遍历文件夹中的所有 mask 文件
    for mask_filename in os.listdir(input_directory):
        if mask_filename.endswith(".png") or mask_filename.endswith(".jpg"):  # 假设 mask 文件为 png 或 jpg 格式
            mask_path = os.path.join(input_directory, mask_filename)

            print(f"Processing {mask_filename}...")
            process_mask_randomly(mask_path, output_directory)


# 调用主函数
if __name__ == "__main__":
    input_directory = "./drew"  # 替换为存放 mask 图像的文件夹路径
    output_directory = "./processed_masks"  # 处理结果保存的目录

    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    process_masks_in_directory(input_directory, output_directory)
