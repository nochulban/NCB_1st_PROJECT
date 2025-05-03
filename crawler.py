import connectDatabase
import os
import boto3
import http.client
import json
import time
import requests
import pymysql
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


# 허용된 확장자 목록
allowed_extensions = {'txt', 'hwp', 'jpg', 'png', 'ppt', 'xlsx'}


#grayhatAPI
def grayhatApi(keyword):
    # 연결 설정
    conn = http.client.HTTPSConnection("buckets.grayhatwarfare.com")

    headers = {
    'Authorization': "Bearer ~~~"
    }
    
    encoded_keyword = quote(keyword)

    # 공식 문서 기반 요청 경로 (파일 키워드 + full path )
    conn.request("GET", f"/api/v2/files?keywords={encoded_keyword}&full-path=1", headers=headers)


    res = conn.getresponse()
    data = res.read()

    try:
        # JSON 파싱
        result = json.loads(data.decode("utf-8"))
        files = result.get("files", [])

        if not files:
            print("[-] 검색된 파일이 없습니다.")
        else:
            # 중복 제거용 버킷 저장 Set
            seen_buckets = set()

            print("[+] 검색된 파일의 버킷 목록:")
            for i, file in enumerate(files, 1):
                bucket = file.get("bucket")
                if bucket and bucket not in seen_buckets:
                    seen_buckets.add(bucket)
                    print(f"[{len(seen_buckets)}] {bucket}")
                    httpsName = "https://" + bucket
                    print(f"✅ Test {"https://" + bucket}")

                    try:
                        existsBucket = connectDatabase.repeatCheck(httpsName)     
                        if existsBucket > 0:
                            print(f"⚠️ 중복된 항목 (이미 존재): {httpsName}")
                            continue
                    except pymysql.MySQLError as e:
                        print("중복 체크 에러:", e)
                        continue

                    # #연결확인 후 Insert
                    # try:        
                    #     response = requests.get(httpsName, headers=headers, timeout=8, stream=True, verify=False)

                    #     if response.status_code == 200: #정상 Insert
                    #         print(f"✅ 연결 가능: {httpsName}")                        
                    #         connectDatabase.bucketUrlInsert(response.status_code, count, httpsName)
                            
                    #     else:                          #에러 Insert
                    #         print(f"✅ 연결 불가: {httpsName}")
                    #         connectDatabase.bucketUrlInsert(response.status_code, count, httpsName)

                    #     print(f"🪣 {name} | 📂 파일 수: {count} | 🔗 {url}")
                    # except Exception as e:
                    #     print(f"❌ 페이지 {httpsName} 접속 확인 중 오류 발생: {e}")

    except Exception as e:
        print(f"[!] 오류 발생: {e}")
        print(data.decode("utf-8"))



#grayhatPageSelenium
def pageSelenium(keyword):
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


    page = 1
    print(f"\n[📄 GrayhatWarfare 버킷 목록 크롤링 시작]\n")

    while True:
        print(f"📄 페이지 {page} ------------------------------")
        if keyword == 'normal':
            base_url = "https://buckets.grayhatwarfare.com/buckets?type=aws&page=" + str(page)

        else:
            encoded_keyword = quote(keyword)
            base_url = f"https://buckets.grayhatwarfare.com/buckets?keywords={encoded_keyword}type=aws&page=" + str(page)
        driver.get(base_url)
        time.sleep(10)

        try:
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 3:
                    name_tag = cols[1].find_element(By.TAG_NAME, "a")
                    count_tag = cols[2].find_element(By.TAG_NAME, "a")

                    name = name_tag.text.strip()
                    count = count_tag.text.strip()
                    url = name_tag.get_attribute("href")

                    httpsName = "https://" + name
                    print(f"✅ Test {"https://" + name}")

                   
                    
                    #중복체크               
                    try:
                        existsBucket = connectDatabase.repeatCheck(httpsName)     
                        if existsBucket > 0:
                            print(f"⚠️ 중복된 항목 (이미 존재): {httpsName}")
                            continue
                    except pymysql.MySQLError as e:
                        print("중복 체크 에러:", e)
                        continue

                    #연결확인 후 Insert
                    try:        
                        response = requests.get(httpsName, headers=headers, timeout=8, stream=True, verify=False)
                        print(f"[{base_url}] 응답 상태 코드: {response.status_code}")

                        if response.status_code == 200: #정상 Insert
                            print(f"✅ 연결 가능: {httpsName}")                        
                            connectDatabase.bucketUrlInsert(response.status_code, count, httpsName)
                            
                        else:                          #에러 Insert
                            print(f"✅ 연결 불가: {httpsName}")
                            connectDatabase.bucketUrlInsert(response.status_code, count, httpsName)

                        print(f"🪣 {name} | 📂 파일 수: {count} | 🔗 {url}")
                    except Exception as e:
                        print(f"❌ 페이지 {httpsName} 접속 확인 중 오류 발생: {e}")
                        
        
        except Exception as e:
            print(f"❌ 페이지 {page} 크롤링 중 오류 발생: {e}")
            
        page += 1
    driver.quit()    
