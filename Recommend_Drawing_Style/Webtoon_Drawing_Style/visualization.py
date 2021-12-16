import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea

def imscatter(x, y, image, ax=None, zoom=1, show_by_thumnail=False, title='webtoon', filename='thumnail.jpg'):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        pass
    im = OffsetImage(image, zoom=zoom)

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

