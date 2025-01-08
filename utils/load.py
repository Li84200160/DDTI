import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms


class DDTIRoughDataset(Dataset):
    def __init__(self, image_directory, mask_directory, transform=None):
        """
        Args:
            image_directory (str): 存放图像文件的目录路径
            mask_directory (str): 存放 mask 文件的目录路径
            transform (callable, optional): 对图像和 mask 应用的变换
        """
        self.image_directory = image_directory
        self.mask_directory = mask_directory
        self.transform = transform

        # 获取图像和 mask 文件名列表
        self.image_files = self._get_files_from_directory(image_directory, ['.jpg', '.png'])
        self.mask_files = self._get_files_from_directory(mask_directory, ['.png', '.jpg'])

        # 找到图像和 mask 文件的交集（不带扩展名进行比较）
        self.common_files = sorted(list(set(self._remove_extensions(self.image_files)) &
                                        set(self._remove_extensions(self.mask_files))))

    def _get_files_from_directory(self, directory, extensions):
        """获取目录下所有指定格式的文件"""
        files = []
        for filename in os.listdir(directory):
            if any(filename.endswith(ext) for ext in extensions):
                files.append(filename)
        return sorted(files)  # 确保文件排序一致

    def _remove_extensions(self, files):
        """去除文件的扩展名以便进行交集比较"""
        return [os.path.splitext(file)[0] for file in files]

    def _load_image(self, image_path):
        """加载图像文件并转换为 RGB 格式"""
        try:
            image = Image.open(image_path).convert("RGB")
            return image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def _load_mask(self, mask_path):
        """加载 mask 文件并转换为灰度图"""
        try:
            mask = Image.open(mask_path).convert("L")
            return mask
        except Exception as e:
            print(f"Error loading mask {mask_path}: {e}")
            return None

    def __len__(self):
        """返回数据集的大小"""
        return len(self.common_files)

    def __getitem__(self, idx):
        """获取指定索引的图像和 mask"""
        common_filename = self.common_files[idx]

        # 拼接带有扩展名的图像和 mask 文件路径
        image_path = os.path.join(self.image_directory, f"{common_filename}.jpg")
        mask_path = os.path.join(self.mask_directory, f"{common_filename}.png")

        image = self._load_image(image_path)
        mask = self._load_mask(mask_path)

        if image is None or mask is None:
            raise ValueError(f"Failed to load image or mask for {common_filename}")

        # 应用变换（如果提供了）
        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)
        mask = mask.squeeze(0)

        return image, mask
