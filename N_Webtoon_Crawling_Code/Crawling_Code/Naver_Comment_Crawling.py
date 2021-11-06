from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import os
import mechanicalsoup
import re
#from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

#해당 장르 연재 작품 수 구하기
# 순정 밥먹고갈래요 안함.
#시대극 삼국지톡 깃허브에 못올림
#19금 만화 안함.
browser = mechanicalsoup.StatefulBrowser()
list_url = 'https://comic.naver.com/webtoon/genre.nhn?genre=sports'
ssoup = browser.open(list_url).soup
title_list = ['nop']
title_num = []
tnum = 0
for tag in ssoup.select('div.list_area li'):
    title = tag.find('a')['title']
    title_list.append(title)
    title_num.append(tnum)
    tnum= tnum+1

title_num.append(tnum)

print(title_list)
print(title_num)

#----------------------------------------------------------------------------

# selenium으로 네이버 웹툰 페이지 불러오기
URL = 'https://comic.naver.com/webtoon/genre.nhn?genre=sports'
os.chdir("C:/Users/user/Downloads/chromedriver_win32")
driver = webdriver.Chrome('chromedriver.exe')
driver.get(URL)

time.sleep(1)


for i in title_num:
    #if i ==1 or i == 2 or i == 3 or i == 4 or i==5 or i ==6 or i==7:
    #    continue

    df = pd.DataFrame(columns=['title','no', 'ID', 'nick', 'content', 'date', 'like', 'dislike'])

    # 전체 웹툰 목록 중 월요일 첫 번째 웹툰으로 페이지 이동
    page = driver.find_elements_by_class_name('thumb')
    page[i].click()

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    button = True
    while button:
        length = driver.find_elements_by_class_name('title')

        # 각 회차를 돌며 댓글 작성자 아이디 수집
        for j in range(len(length)):
            # 해당 페이지의 회차 모두 가져오기
            titlenum = driver.find_elements_by_class_name('title')

            time.sleep(0.5)

            webnum = [y.text for y in titlenum]
            enterToon = driver.find_elements_by_partial_link_text(webnum[j])

            time.sleep(0.5)

            enterToon[0].click()

            # 현재 댓글 부분 파싱이 안되는 설정이므로 src의 댓글창 페이지로 직접 이동
            # 현재 URL주소 복사
            html = driver.current_url
            currentPage = html[html.find('?'):]

            # 댓글창 페이지 URL
            URL2 = 'https://comic.naver.com/comment/comment.nhn' + currentPage
            print('Title:', title_list[i], i, ' : ', URL2)
            no = currentPage.split('&')[1]
            no = re.sub('no=','',no)

            title = title_list[i]
            time.sleep(0.4)

            # 댓글창 페이지 열기
            driver2 = webdriver.Chrome('chromedriver.exe')
            driver2.get(URL2)

            time.sleep(3)

            while True:
                try:
                    # 수집 편의를 위해 클린봇 댓글 필터링 기능 해제
                    driver2.find_element_by_class_name('u_cbox_cleanbot_setbutton').click()
                    time.sleep(0.3)
                    driver2.find_element_by_class_name('u_cbox_layer_cleanbot_checkbox').click()
                    time.sleep(0.3)
                    driver2.find_element_by_class_name('u_cbox_layer_cleanbot_extrabutton').click()
                    time.sleep(0.3)
                    break

                except:
                    driver2.close()
                    driver2 = webdriver.Chrome('chromedriver.exe')
                    driver2.get(URL2)
                    print('driver2 ERROR')
                    time.sleep(20)
                    break

            time.sleep(3)
            # 전체 댓글 보기 클릭 & 아이디 목록 수집
            driver2.find_element_by_partial_link_text('전체댓글').click()

            #except NoSuchElementException:
            #    time.sleep(1)
            #    continue

            time.sleep(3)

            # 최신 댓글부터 가장 나중의 댓글까지 창 이동하며 아이디 목록 수집
            num = 0
            start = 0
            error_back = 0
            while True:
                try:
                    while start <= 0:

                        time.sleep(0.4)

                        page = driver2.find_elements_by_class_name('u_cbox_num_page')
                        #print('now page: ', int(page[num].text), ' index: ', num)

                        idd = driver2.find_elements_by_class_name('u_cbox_id')
                        time.sleep(0.1)
                        nickk = driver2.find_elements_by_class_name('u_cbox_nick')
                        time.sleep(0.1)
                        chat = driver2.find_elements_by_class_name('u_cbox_contents')
                        time.sleep(0.1)
                        date = driver2.find_elements_by_class_name('u_cbox_date')
                        time.sleep(0.1)
                        like = driver2.find_elements_by_class_name('u_cbox_cnt_recomm')
                        time.sleep(0.1)
                        dislike = driver2.find_elements_by_class_name('u_cbox_cnt_unrecomm')
                        time.sleep(0.1)

                        while len(idd)>0:
                            results = [(title,no, idd[0].text, nickk[0].text, chat[0].text, date[0].text, like[0].text, dislike[0].text)]
                            dfnew = pd.DataFrame(results,columns=['title','no','ID','nick','content','date','like','dislike'])
                            df= df.append(dfnew,ignore_index=True)
                            idd.pop(0)
                            nickk.pop(0)
                            chat.pop(0)
                        time.sleep(0.1)

                        # 페이지가 10의 배수이면 다음 페이지 클릭, 동일 과정 거침
                        try:
                            a = driver2.find_elements_by_class_name('u_cbox_next')  # *****CLEAR v
                            if (int(page[num].text) % 10 == 0 and a[0].text != ''):
                                driver2.find_element_by_class_name('u_cbox_next').click()
                                time.sleep(0.1)
                                page = driver2.find_elements_by_class_name('u_cbox_num_page')
                                time.sleep(0.1)
                                idd = driver2.find_elements_by_class_name('u_cbox_id')
                                time.sleep(0.1)
                                nickk = driver2.find_elements_by_class_name('u_cbox_nick')
                                time.sleep(0.1)
                                chat = driver2.find_elements_by_class_name('u_cbox_contents')
                                time.sleep(0.1)
                                date = driver2.find_elements_by_class_name('u_cbox_date')
                                time.sleep(0.1)
                                like = driver2.find_elements_by_class_name('u_cbox_cnt_recomm')
                                time.sleep(0.1)
                                dislike = driver2.find_elements_by_class_name('u_cbox_cnt_unrecomm')
                                a.clear()
                                time.sleep(0.1)

                                while len(idd)>0:
                                    results = [(title, no, idd[0].text, nickk[0].text, chat[0].text, date[0].text, like[0].text, dislike[0].text)]
                                    dfnew = pd.DataFrame(results,columns=['title', 'no','ID', 'nick', 'content', 'date', 'like', 'dislike'])
                                    df = df.append(dfnew, ignore_index=True)
                                    idd.pop(0)
                                    nickk.pop(0)
                                    chat.pop(0)

                                num = 0
                                print('now page: ', int(page[num].text), ' index: ', num)

                        except IndexError:
                            break

                        num += 1

                        time.sleep(0.4)

                        try:
                            page[num].click()

                        except IndexError:
                            break

                        page.clear()
                        idd.clear()
                        time.sleep(0.1)

                    # 댓글 페이지 닫기
                    error_back = 0
                    driver2.close()
                    break

                except IndexError:
                    break

                except:
                    print('ERROR')
                    error_back += 1
                    if (error_back > 10):
                        break
                    continue

            time.sleep(0.4)

            # 페이지 뒤로 가기, 다시 만화 목록으로
            driver.back()
            time.sleep(1)
            titlenum.clear()
            # time.sleep(0.5)
            enterToon.clear()

        length.clear()
        if (driver.find_elements_by_class_name('next')):
            button = True
            driver.find_element_by_class_name('next').click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        else:
            button = False

    # 전체 정식연재 만화 창으로 이동
    time.sleep(1)
    print(title_list[i], "end")
    name = 'N_Webtoon_3_comment_sports_' + str(title) + '.csv'
    name = "".join(i for i in name if i not in "\/:*?<>|")
    df.to_csv(name, encoding='utf-8-sig')
    del df

    driver.get(URL)

    time.sleep(0.5)
    page.clear()
    time.sleep(0.5)