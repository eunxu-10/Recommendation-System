from multiprocessing import Pool
import pandas as pd
import requests
import time

def getReplyDf(ls_url_id):
    print('Getting webtoon`s entire comments list from Daum..')

    headers = {'Content-Type': 'text/html'}
    cookies = {
        'session_id': 'RECENT_USE=on; RECENT_SEARCH=%EC%8C%8D%EA%B0%91%2C; RECENT_VIEW=105701|54701|104995|50615|90827; SLEVEL=0; ALARM_COUPON=20210315192117; __T_=1; VOTE=MTAuNTE%3D; MY=MTAuNTE%3D; ORDER=MTAuNTE%3D; HM_CU=5DRHdXDNCXg; PROF=0603012032024076024120UiQPJk7X-6w0mlxoempuua-WtEc2RT95vdkDQkloQ8t.KuZP3z7wEl2bxriNh5SdkQ00LYYSA9A1_cGNLCyhCzrwOjTi9JCLCPIz3mlNTt7zkh799Fe9fQCTuFahgZwN7arRuq1D_iaAuoc0fIauQlo8OTLcCscrxJX8Uw00rfhTzfRpBVHPn23B_vTzGDH5t.ow35ZYntxYtQOcleZXKh2-G69UsZ5Joi8PC77SepzPx_EoF25QUPUbuh6eoCQZjRxg2d7oLS_CliiS.l83vhtpaXRyxA00; AGEN=4ywGKJy_PaRaCTDlmS0HW-WYwYc1j29NCjAYA-_LArc; TIARA=-73vHQQZIRxfdXAvj44dQwwavwjLg6nvVGXEtrCIlZXu863u25mi8mC7Y9bO.h-EsfrP1HeF.yELGzHaPO31P81NuBns.l5W; TS=1615950634; HTS=bVfL1dMfBsVxzsj8gVzI5g00; LSID=504abe8c-6e68-42db-bbd8-2af123c1d5c21615950634905; _fbp=fb.1.1615950639787.830177619; _T_ANO=OKZ+Q7Y4USXeyLVg1FxHtaULMyth/41zPwjH70cY9uaj3fZxApYc3Gyg9+qIuDbYCMYz4PErFebItCEXrE4FgQxYjtA9vUB2VsgDa0sWRapm8NuIqTsv7//6qVc8QDmjPW50kHWVY7ace5tdJ4Cli3uJ09HbrYl/Av/2SD/oo+eXt4qt+GHkqWS1/Mkch0h5ZNzmgcXcfsekrvv6S76JrB/DznWm5G+2pA+QUGK/LUgeLB0qQ8shpQI0MBB9O8cFE6Kp9X1kLiaSbFfgJkYuUgCEYVEO1+Xvcd29B7wC0wzohhBaiCZQCTcbh4DgEb7fd9Uxb3qr7RicroD5HEdUCw=='}

    cnt = 0
    error = 0
    error_ls = []

    wbt_comment = pd.DataFrame(columns=['commentId', 'parentCommentId', 'articleId', 'articleType', 'subject',
                                        'viewUrl', 'encryptedUserId', 'daumName', 'childCount', 'recommendCount',
                                        'disagreeCount', 'status', 'regDate', 'content', 'spoiler', 'isWithdraw',
                                        'isParent', 'isMine', 'isBest'])
    for chapterid in ls_url_id:
        # 댓글
        try:
            url3 = 'http://m.cartoon.media.daum.net/data/gateway/comments/list/webtoon_ep/' + str(
                chapterid) + '?page=1&pageSize=99999&isBest=true&sortType=Recommend'
            response = requests.get(url3, headers=headers, cookies=cookies)
        except:
            print("server rejected please wait 15sec...")
            time.sleep(15)
            print("now reconnect again...", end="")
            url3 = 'http://m.cartoon.media.daum.net/data/gateway/comments/list/webtoon_ep/' + str(
                chapterid) + '?page=1&pageSize=99999&isBest=true&sortType=Recommend'
            response = requests.get(url3, headers=headers, cookies=cookies)
            print("success!!")

        try:
            temp_df = response.json()
            for i in temp_df['data']['comments']:
                wbt_comment = wbt_comment.append(i, ignore_index=True)

        except:  # 에러발생시 어떤 웹툰의 회차인지 캐치
            error += 1
            print("error occurd!!(", error, '-', chapterid, ")..", end="")
            error_ls.append(chapterid)

        if cnt % 5 == 0:
            print(cnt, "(", chapterid, ").", end="")
        cnt += 1

    df = wbt_comment[['commentId',  # 댓글 id #'parentCommentId',
                      'articleId',  # 회차 id #'articleType',
                      'subject',  # 웹툰 제목 # 'viewUrl','encryptedUserId',
                      'daumName',  # 작성자 name # 'childCount',
                      'recommendCount', 'disagreeCount',
                      # 'status',
                      'regDate',  # 댓글 작성 시간
                      'content',  # 내용
                      # 'isParent',
                      'isBest'  # 베댓 여부
                      ]]
    return df.reset_index(drop=True)

if __name__ == '__main__':
    start_time = time.time()
    data = pd.read_csv("D_Webtoon_2_thumbnail.csv")
    pool = Pool(processes=4)  # 4개의 프로세스 동시에 작동
    li = list(data['id'])[0:101]
    df3 = pd.concat(pool.map(getReplyDf, [li]))
    pool.close()
    pool.join()
    df3.to_csv("D_Webtoon_3_comments(0-30).csv", index=False)
    print("실행 시간 : %s초" % (time.time() - start_time))
