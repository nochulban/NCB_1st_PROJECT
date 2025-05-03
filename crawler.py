import connectDatabase
import os
import boto3
import http.client
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from urllib.parse import quote
from hashlib import sha256
from datetime import datetime
from botocore.exceptions import ClientError


# Chrome 옵션 설정 (Windows에서도 헤드리스로 작동)
options = Options()
options.add_argument("--headless=new")  # 최신 방식의 헤드리스 모드
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")


# 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
headers = {"User-Agent": "Mozilla/5.0"}  # 요청 차단 우회용 헤더
browser = webdriver.Chrome(options=options)


# 허용된 확장자 목록
allowed_extensions = {'txt', 'hwp', 'jpg', 'png', 'ppt', 'xlsx'}

#grayhatAPI


#grayhatPageSelenium


#



if __name__=="__main__":
    print("키워드를 입력하세요 : ")
    keyword = input()

    print(keyword)
    print(type(keyword))
