import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea

def imscatter(x, y, image, ax=None, zoom=1, show_by_thumnail=False, title='webtoon', filename='thumnail.jpg'):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)

    # Convert inputs to arrays with at least one dimension. 입력 값을 1 차원 이상의 배열로 변환합니다.
    # 스칼라 입력은 1 차원 배열로 변환되는 반면 더 높은 차원의 입력은 유지됩니다.
    x, y = np.atleast_1d(x, y)

    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)

        if show_by_thumnail:
            offsetbox = TextArea(title, minimumdescent=False)
            ac = AnnotationBbox(offsetbox, (x0, y0),
                                xybox=(20, -40),
                                xycoords='data',
                                boxcoords="offset points")
            artists.append(ax.add_artist(ac))
        artists.append(ax.add_artist(ab))

    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()

    return artists

