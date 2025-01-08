import os
import xmltodict
import json
from PIL import Image, ImageDraw


# 加载XML文件
def load_xml(file_path):
    with open(file_path, 'r') as file:
        return xmltodict.parse(file.read())


# 根据svg坐标生成mask
def create_mask(image_size, points):
    mask = Image.new('L', image_size, 0)  # L代表灰度图
    draw = ImageDraw.Draw(mask)
    polygon = [(point['x'], point['y']) for point in points]
    draw.polygon(polygon, outline=255, fill=255)
    return mask


# 保存mask图像
def save_mask(image_mask, output_path):
    image_mask.save(output_path)


# 解析并生成mask
def process_case(case_data, image_directory, output_directory):
    number = case_data.get('number', [])
    marks = case_data.get('mark', [])
    if not isinstance(marks, list):
        marks = [marks]  # 如果只有一个mark，将其转换为列表

    for mark in marks:
        svg_data = mark['svg']
        svg_list = json.loads(svg_data)

        # 查找对应的图像文件
        image_filename = f"{number}_1.jpg"  # 假设图像的命名规则是 "{image_number}_1.jpg"
        image_path = os.path.join(image_directory, image_filename)

        if not os.path.exists(image_path):
            print(f"Image {image_filename} not found, skipping...")
            continue

        # 打开图像并获取尺寸
        with Image.open(image_path) as img:
            image_size = img.size  # 获取图像尺寸 (width, height)
            print(f"Processing image {image_filename} with size {image_size}")

            # 为每个标注生成mask
            for idx, svg in enumerate(svg_list):
                points = svg['points']
                mask = create_mask(image_size, points)

                # 创建输出目录（如果不存在）
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                # 保存mask到指定目录
                mask_output_path = os.path.join(output_directory, f"{number}_{idx+1}.png")
                save_mask(mask, mask_output_path)
                print(f"Saved mask for image {number}, region {idx}, to {mask_output_path}")


# 遍历目录并处理XML文件
def process_directory(directory_path, image_directory, output_directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            xml_path = os.path.join(directory_path, filename)
            print(f"Processing XML: {xml_path}")

            # 处理XML文件
            try:
                xml_data = load_xml(xml_path)
                cases = xml_data.get('case', [])
                if not isinstance(cases, list):
                    cases = [cases]

                # 处理每一个case
                for case in cases:
                    process_case(case, image_directory, output_directory)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")


# 主函数
def main():
    xml_directory = '../data'  # 替换为存放XML文件的目录路径
    image_directory = '../data'  # 替换为存放JPG图片的目录路径
    output_directory = './drew'  # 替换为存放生成的mask的目录路径

    process_directory(xml_directory, image_directory, output_directory)


if __name__ == "__main__":
    main()
