# NAVER CLOUD CAMP 정보보안 3기 3조 NOCHULBAN (1차 프로젝트)
## 공개 출처 정보 API 호출 및 자동화 탐색 기반 클라우드 오브젝트 스토리지 내 문서 유출 탐지 시스템 개발
<div align="center">
  <img src="https://github.com/user-attachments/assets/a3819795-5724-472c-a233-5d41daca6ed9" width="500"/>
</div>

## 프로젝트 개요
본 프로젝트는 GrayhatWarfare API 및 Selenium을 활용해 공개된 S3 버킷 내 문서를 수집하고, 수집된 문서 목록을 기반으로 유출 가능성이 있는 파일을 자동으로 탐지·기록하는 시스템입니다.

## 주요 기능
- S3 버킷 크롤링(GrayhatWarfare API 및 Selenium 기반)
- 특정 키워드 기반 파일 탐색
- 메타데이터 수집 및 DB 저장
- 유출 파일 보고서 자동 생성(GPT API 연동)
- PDF 기반 보고서 생성

## 사용 기술
- Python 3.10
- Selenium
- pymysql
- FPDF
- OPENAI API (GPT)
- MySQL

## 디렉터리 구조
```
ncb/
├── /venv                     # 가상환경
├── main.py                   # 키워드 입력 후 전체 파이프라인 실행
├── gpt_report.py             # GPT 기반 보고서 자동화
├── connectDatabase.py        # DB 연결 및 쿼리 처리
├── crawler.py                # 공개 버킷 크롤러(Grayhat, Selenium)
├── output/                   # 생성된 보고서 저장 경로
└── requirements.txt          # 의존성 목록
```

## 실행 방법 (api key 추가 필요)
```
# 가상환경 생성 및 실행
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 파이프라인 실행
python main.py
```

## 데이터베이스 구성
- buckets : 버킷 메타 정보
- documents : 파일 메타정보(경로, 해시 등)
<div align="center">
  <img width="883" alt="스크린샷 2025-05-08 오전 11 23 19" src="https://github.com/user-attachments/assets/5fd3f93e-7c6c-454e-ba66-f9dcf8834eb6" />
</div>

## 시연 영상
https://youtu.be/jGol5wmgGyY?si=5GjYbJhN5YIyr8EB
