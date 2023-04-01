from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os

file = os.listdir("./D_thumb_img_wbt")
wbt_id = []
for f in file:
    wbt_id.append(f[:-4])

np_points = np.load("./avg_list.npy")
points = pd.DataFrame(np_points)

# k-means clustering 실행
kmeans = KMeans(n_clusters=12)
kmeans.fit_predict(points)

# 결과 확인
result_by_sklearn = pd.DataFrame(columns=['wbt_id', 'x', 'y', 'cluster'])
result_by_sklearn['wbt_id'] = wbt_id
result_by_sklearn['x'] = points[0]
result_by_sklearn['y'] = points[1]
result_by_sklearn["cluster"] = kmeans.labels_
result_by_sklearn.to_csv("12_means_clustering_final_predict.csv")
print(result_by_sklearn)