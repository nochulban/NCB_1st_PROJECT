# NOCHULBAN (1차 프로젝트)
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
