import os
import numpy as np

def imgList():
    thumnail_path = "./D_thumb_img_chap_class"
    wbt_path = "./D_thumb_img_wbt"
    wbt_img = []

    for img in os.listdir(thumnail_path):
      wbt_img.append(os.path.join(wbt_path,img+".png"))
    wbt_img.sort()

    return wbt_img

def avgList(result, label_arr):

    avg_list = []
    scatter_x = result[:, 0]
    scatter_y = result[:, 1]
    group = np.array(label_arr)

    for g in np.unique(group):
        i = np.where(group == g)
        x_avg = np.mean(scatter_x[i])
        y_avg = np.mean(scatter_y[i])
        avg_list.append((x_avg, y_avg))

    return avg_list