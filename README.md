# Recommendation-System
:books: korean webtoon recommendation system
(Naver and Daum)

## 프로젝트 개요
여러 웹사이트의 웹툰을 통합하여 추천해주는 웹사이트 개발을 목표로 진행하였다. 
추천은 장르, 그림체로 이루어지며 그림체 추천을 위해 style transfer, k means clustering 등의 알고리즘을 사용하였다. 
결론적으로 좋아하는 만화를 검색하면 이와 비슷한 장르의 만화를 별점 순으로 추천해주거나 좋아하는 그림체를 선택하면 이와 비슷한 그림체의 만화를 추천해주는 웹사이트를 개발하였다.


## 프로젝트 소개 & 시연 영상
[![이미지](https://img.youtube.com/vi/QH6CKN6mb8M/0.jpg)](https://www.youtube.com/watch?v=QH6CKN6mb8M&t=0s)

## Code Components
```
├── D_Webtoon_Crawling_Code
│   ├── Daum_comment_crawling_multiprocessing.py
│   ├── Daum_comment_crawling.ipynb
│   ├── Daum_thumbnail_crawling.ipynb
│   └── Daum_toonsinfo_crawling.ipynb
├── N_Webtoon_Crawling_Code
│   ├── Naver_comment_crawling.py
│   ├── Naver_thumbnail_crawling.py
│   └── Naver_toonsinfo_crawling.py
├── Recommend_Drawling_Style
│   ├── Webtoon_Drawling_Style
│   │   ├── Classify_cluster.ipynb
|   │   ├── k_means_clustering.py
│   │   ├── loss.py
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── train.py
│   │   ├── utils.py
│   │   └── visualization.py
│   ├── download_n_webtoon_images.ipynb
│   └── download_d_webtoon_images.ipynb
├── README.md
├── Genre_Recommendation_Code.ipynb
└── README.md
```

## How to Use
### 그림체 추천
#### 그림체 추출
```
cd Recommed_Drawing_Style/Webtoon_Drawling_Style
pip install -r requirements.txt
python main.py
```
#### 비슷한 그림체끼리 묶기
```
python k_means_clustering.py
python classify_cluster.py
```
