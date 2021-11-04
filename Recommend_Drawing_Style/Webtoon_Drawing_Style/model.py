import torch.nn as nn
import torchvision.models as models

class Resnet(nn.Module):

    def __init__(self):
        super(Resnet,self).__init__()
        resnet = models.resnet50(pretrained=True)
        self.layer0 = nn.Sequential(*list(resnet.children())[0:1])
        self.layer1 = nn.Sequential(*list(resnet.children())[1:4])
        self.layer2 = nn.Sequential(*list(resnet.children())[4:5])
        self.layer3 = nn.Sequential(*list(resnet.children())[5:6])

    def forward(self,x):
        out_0 = self.layer0(x)
        out_1 = self.layer1(out_0)
        out_2 = self.layer2(out_1)
        out_3 = self.layer3(out_2)

        return out_0, out_1, out_2, out_3