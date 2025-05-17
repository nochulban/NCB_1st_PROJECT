# NAVER CLOUD CAMP 정보보안 3기 3조 NOCHULBAN (2차 프로젝트)
## 공개 출처 기반 수집 파일에 대한 악성코드 탐지 시스템 개발
<div align="center">
  <img src="https://github.com/user-attachments/assets/a3819795-5724-472c-a233-5d41daca6ed9" width="500"/>
</div>

## 프로젝트 개요
본 프로젝트는 공개된 S3 버킷에서 수집된 문서를 대상으로 VirusTotal API 기반 악성코드 탐지를 수행하고, 탐지 결과를 기반으로 자동 보고서를 생성하는 시스템입니다.
기존 1차 프로젝트의 유출 의심 탐지 기능에 더해, 공격 가능성이 있는 문서를 식별하고 보안 보고서로 정리하는 데 중점을 둡니다.

## 주요 기능
- S3 버킷 크롤링 및 파일 자동 다운로드
- VirusTotal API 기반 악성코드 탐지
- 탐지 결과 DB 저장 및 자동화 보고서 생성
- PDF 기반 결과 보고서 출력


## 사용 기술
- Python 3.10
- requests, pymysql, hashlib
-	VirusTotal API
-	FPDF
-	OPENAI API (GPT 기반 문서 자동화)
-	MySQL
  
## 디렉터리 구조
```
ncb/
├── main.py                   # 전체 파이프라인 실행
├── virusTotalHash.py         # VT API 기반 해시 조회 및 분석
├── crawledDataDownload.py    # S3에서 실제 파일 다운로드
├── gpt_report.py             # GPT 기반 보고서 자동화
├── connectDatabase.py        # DB 연결 및 쿼리 처리
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
- malware_docs : 악성 탐지된 문서 정보 (탐지 명세 포함)
<div align="center">
  <img width="932" alt="스크린샷 2025-05-17 오후 2 57 08" src="https://github.com/user-attachments/assets/8112ddf9-c58d-4f8b-b35d-c65320d0e491" />
</div>
