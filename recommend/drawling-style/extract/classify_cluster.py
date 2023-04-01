import pandas as pd
import pickle

data = pd.read_csv("12_means_clustering_final_predict.csv")

cluster = {}
for i in range(12):
    cluster[i] = []
for i in range(12):
    cluster[i] = data[data['cluster']==i]['wbt_id'].tolist()

with open('cluster_12_final_predict.pickle', 'wb') as fw:
    pickle.dump(cluster, fw)