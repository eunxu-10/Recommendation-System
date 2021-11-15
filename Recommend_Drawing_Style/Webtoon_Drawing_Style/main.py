import matplotlib.pyplot as plt
from model import Resnet
from train import style_extract, tsne
from utils import imgList, avgList
from visualization import imscatter
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import numpy as np

def main():
    resnet = Resnet().cuda()
    for param in resnet.parameters():
        param.requires_grad = False

    wbt_data = datasets.ImageFolder("./D_thumb_img_chap_class", transform=transforms.ToTensor())
    class_to_idx = wbt_data.class_to_idx
    idx_to_class = {}
    for key, value in enumerate(class_to_idx):
        idx_to_class[key] = value

    total_arr, label_arr = style_extract(wbt_data, resnet)
    # print(len(total_arr)) # 79488
    
    total_result = np.array([])
    len_total_arr = len(total_arr)
    for step in range(0, len_total_arr, 800):
        result = tsne(total_arr[step:step+800], 2, 100)
        if step ==0:
            total_result = result
        else:
            total_result = np.vstack((total_result, result))
            
    avg_list = avgList(total_result, label_arr)
    np_avg_list = np.array(avg_list)
    np.save("./avg_list", np_avg_list)
    
    wbt_img = imgList()
    for i in range(len(avg_list)):
        img_path = wbt_img[i]
        imscatter(avg_list[i][0], avg_list[i][1], image=img_path, zoom=0.4, show_by_thumnail=True,
                  title=idx_to_class[i])
    plt.savefig("visualization_by_thumnail.jpg")

if __name__ == '__main__':
    main()