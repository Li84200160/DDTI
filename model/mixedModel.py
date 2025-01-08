import torch
import torch.nn as nn
import torch.nn.functional as F

class MixedSegmentation(nn.Module):
    def __init__(self, modelUp, modelDown):
        super(MixedSegmentation, self).__init__()
        self.modelUp = modelUp
        self.modelDown = modelDown

    def forward(self, x1, x2):
        combine = x1 + x2
        # load 自监督权重
        y = self.modelUp(x1)
        preciseMask = self.modelDown(combine)

        return y, preciseMask
