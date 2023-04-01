import pandas as pd
import re
import mechanicalsoup

df = pd.DataFrame(columns=['title','finishYn','ageGrade','Score','artist','latest_upload','page url','intro','genres','form'])
browser = mechanicalsoup.StatefulBrowser()

list = ['daily', 'comic', 'fantasy', 'action', 'drama', 'pure', 'sensibility', 'thrill', 'historical', 'sports']

for genre in list:
    list_url = 'https://comic.naver.com/webtoon/genre.nhn?genre=' + str(genre)
    soup = browser.open(list_url).soup
    for tag in soup.select('div.list_area li'):
        url = str("http://comic.naver.com") + tag.find('a')['href']
        title = tag.find('a')['title']
        artist = re.sub('\n', '', tag.select('dd.desc')[0].text)
        date_0 = re.sub('\n', '', tag.select('dd.date2')[0].text)
        star = re.sub('평점\n','', tag.select('div.rating_type')[0].text)
        date_1 = re.sub('\r', '', date_0)
        date_2 = re.sub('\t', '', date_1)
        if tag.select('div.thumb img.finish'):
            finish = 'Y'
        else :
            finish = 'N'
        if tag.select('div.thumb span.ico_cut'):
            cuttoon = tag.select('div.thumb span.ico_cut')[0].text
        else :
            cuttoon = 'scroll'

        url_soup = browser.open(url).soup
        body = url_soup.select('div.detail p')[0].text
        body_1 = re.sub(r'^\s+', '', body)
        body_2 = re.sub('\n', ' ', body_1)
        body_3 = " ".join(body_2.split())
        age = url_soup.select('div.detail p.detail_info span.age')[0].text

        results = [(title, finish,  age, star, artist, date_2, url, body_3,genre,cuttoon)]
        dfNew = pd.DataFrame(results, columns=['title','finishYn','ageGrade','Score','artist','latest_upload','page url','intro','genres','form'])
        df = df.append(dfNew,ignore_index=True)
############################################크롤링 끝############################################
df.to_csv('N_Webtoon_1_toonsinfo.csv', encoding = 'utf-8-sig')