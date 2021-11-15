from loss import GramMatrix
import torch
from sklearn.manifold import TSNE


def style_extract(data, resnet):
    total_arr, label_arr = [], []

    for idx,(image, label) in enumerate(data):
        i = image.cuda()
        i = i.view(-1,i.size()[0], i.size()[1], i.size()[2])

        style_target = list(GramMatrix().cuda()(i) for i in resnet(i))

        arr = torch.cat([style_target[0].view(-1),style_target[1].view(-1),style_target[2].view(-1),style_target[3].view(-1)],0)
        gram = arr.cpu().data.numpy().reshape(1,-1)

        total_arr.append(gram.reshape(-1))
        label_arr.append(label)

        if idx % 50 == 0 and idx != 0:
          print(f'{idx} images style feature extracted..[{round(idx / len(data), 2) * 100}%]')
    print("\nImage style feature extraction done.\n")

    return total_arr, label_arr

def tsne(total_arr, n_components, perplexity):
    # n_components=2: 2차원으로 차원 축소
    model = TSNE(n_components=2, init='pca',random_state=0, verbose=3, perplexity=100)
    result = model.fit_transform(total_arr)

    return result