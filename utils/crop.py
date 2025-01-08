from torchvision.transforms import functional as F
from PIL import Image

class CropSquare:
    def __call__(self, image):
        """
        从矩形裁剪为最大的正方形。
        """
        if not isinstance(image, Image.Image):
            raise TypeError(f"Input should be a PIL Image. Got {type(image)}")

        # 获取图像的宽和高
        width, height = image.size

        # 计算正方形的边长
        square_size = min(width, height)

        # 计算左上角坐标
        left = (width - square_size) // 2
        top = (height - square_size) // 2

        # 裁剪并返回图像
        return image.crop((left, top, left + square_size, top + square_size))
