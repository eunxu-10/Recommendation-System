import pandas as pd
import re
import mechanicalsoup
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time

os.chdir("C:/Users/김은수")
df = pd.DataFrame(columns=['title','thumb','epi_title'])
browser = mechanicalsoup.StatefulBrowser()
driver = webdriver.Chrome('chromedriver.exe')

list = ['daily', 'comic', 'fantasy', 'action', 'drama', 'pure', 'sensibility', 'thrill', 'historical', 'sports']

df = pd.DataFrame(columns=['title','episode_title','img_url'])

for genre in list:
    list_url = 'https://comic.naver.com/webtoon/genre.nhn?genre=' + str(genre)
    soup = browser.open(list_url).soup

    for tag in soup.select('div.list_area li'):
        url = str("http://comic.naver.com") + tag.find('a')['href']
        title = tag.find('a')['title']

        driver.get(url)
        title = tag.find('a')['title']
        url_soup = browser.open(url).soup

        while url_soup.select('a.next'):
            for tag2 in url_soup.select('tr'):
                if tag2.find('img') == None:
                    continue
                else:
                    thumb = tag2.find('img')['src']
                    epi_title = tag2.find('img')['alt']
                    results = [(title,epi_title,thumb)]
                    dfNew = pd.DataFrame(results, columns=['title','episode_title','img_url'])
                    df = df.append(dfNew,ignore_index=True)
            time.sleep(0.4)
            driver.find_element_by_class_name('next').click()
            url = driver.current_url
            url_soup = browser.open(url).soup

############################################크롤링 끝############################################
df.to_csv('N_Webtoon_2_thumbnail.csv', encoding = 'utf-8-sig')