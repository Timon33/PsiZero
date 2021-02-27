import torch
import torch.nn as nn


class NN(torch.nn.Module):

    def __init__(self, inputs: int):
        super().__init__()

        self.l1 = nn.Linear(inputs, 512)
        self.l2 = nn.Linear(512, 256)
        self.l3 = nn.Linear(256, 128)
        self.l4 = nn.Linear(128, 1)

    def forward(self, x):
        x = self.l1(x)
        x = self.l2(x)
        x = self.l3(x)
        x = self.l4(x)
        return x