#!/usr/bin/python
#-*- encoding: utf-8 -*-
import requests as rs
import bs4
import time
#csv 파일 입출력
import csv
import re
from io import StringIO
from operator import itemgetter
from datetime import datetime, date, timedelta

class Crawling:
    def getDateOnBoard(self, date):
        '''
        받은 날짜(YYYY.MM.DD)를 YYYYMMDD 문자열로 반환한다.
        '''
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        return year + month + day
    def getDate(self, d):
        '''
        날짜 데이터를 YYYYMMDD 형식으로 뽑아준다
        '''
        today = str(d.year)
        mon = ''
        if len(str(d.month)) < 2:
            mon = '0' + str(d.month)
        else:
            mon = str(d.month)
        today = today + mon
        day = ''
        if len(str(d.day)) < 2:
            day = '0' + str(d.day)
        else:
            day = str(d.day)
        today = today + day
        return today
    def getContent(self, list):
        """
        BS4로 추출된 영화 URL에서 내용물을 뽑아내고, csv파일로 저장한다.
        반환형 :
        list : url_lists
        result : 결과값
        """
        result = False
        count = 0
        cookie = None
        results = []
        #감정 사전 로드
        with open("polarity.txt", "r") as polarity:
            dic = []
            cr = csv.reader(polarity)
            for row in cr:
                dic.append(row)
        #영화 평점 및 코멘트 저장 공간 로드
        with open("temp.csv", "w") as csv_file:
            cw = csv.writer(csv_file, delimiter='|')
            cw.writerow(["title", "rate", "text", "pos", "neg"])
            for index, movie_url in enumerate(list):
                #영화 제목
                title = self.getTitle(movie_url)
                #영화당 평점 페이지 갯수
                pages = self.getPage(movie_url)
                #페이지별 모든 평가를 긁음
                print("영화 %s는 총 %d개의 평가페이지가 존재합니다."%(title, pages))
                for page in range(pages):
                    reply_urls = "http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=" + \
                                 self.getCode(movie_url) + "&type=after&page=" + str(page+1)
                    print("영화 %s의 평가 페이지 %d번째"%(title, page+1))
                    response = rs.get(reply_urls.encode('utf-8'))
                    html_content = response.text.encode(response.encoding);
                    navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
                    #평가 및 코멘트 추출 준비
                    content = navigator.find("div", {"class":"score_result"})
                    #페이지가 존재할 경우 추출
                    if content is not None:
                        #평점
                        rates = content.find_all("div", {"class":"star_score"})
                        for rate in rates:
                            rate = rate.em.get_text().replace("\"\r\n\t", '')
                            results.append([title, rate])
                        #코멘트
                        texts = content.find_all("div", {"class":"score_reple"})
                        for text in texts:
                            text = text.p.get_text().replace("BEST", '').replace("관람객", '').replace("\"\r\n\t", '')
                            results[count].append(self.getText(text))
                            resultText = '[%d번째 평가] 영화 : %s 평점 : %s, 내용 : %s'%\
                                          (count+1, results[count][0], results[count][1], results[count][2])
                            print(resultText)
                            results[count] += self.getEval(results[count][2], dic)
                            cw.writerow(results[count])
                            #주소 및 갯수 카운터 +1
                            count += 1
                            if count >= 39:
                                return results

        return results
    def getBoard(self):
        """
        BS4, request를 활용하여 URL별 존재하는 상영중인 영화
        주소를 리스팅한다.
        """
        today = datetime.today()
        #DC 프갤 주소
        dcp_url = "http://gall.dcinside.com/board/lists/?id=programming"
        for page in range(pages):
            #페이지마다 요청
            dcp_url += "&page=" + page
            response = rs.get(dcp_url)
            #응답으로 부터 HTML 추출
            html_content = response.text.encode(response.encoding);
            #HTML 파싱
            navigator = bs4.BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
            #네비게이터를 이용해 원하는 링크 리스트 가져오기
            rows = navigator.find("tr", {"class":"tb"})
            #글이 존재하는지 확인하고 각각 상영작들의 주소를 추출
            if rows is not None:
                url_lists = []
                dates = rows.find_all("td", {"class":"t_date"})
                links = rows.find_all("td", {"class":"icon_pic_n"})
                for index, date in enumerate(dates):
                    #오늘날짜와 게시글의 날짜가 같다면
                    if self.getDateOnBoard(date) == self.getDate(today):
                        url_lists.append(links[index])
            #URL 출력
            for index, url_list in enumerate(url_lists):
                resultText = '[%d개] %s'%(index+1, url_list)
                print(resultText)
            return url_lists
