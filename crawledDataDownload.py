import boto3
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__))) #경로 최소화 시 필요

# .env 파일 로드 (AWS 자격 증명 불러오기)
load_dotenv()

# 환경 변수에서 자격 증명 가져오기
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = ''  # 예: ap-northeast-2 (서울 리전)

# S3 클라이언트 생성
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# 🪣 버킷 이름: https://jaeyoon-example.s3-ap-northeast-2.amazonaws.com/
#bucket_name = 'jaeyoon-example'

# 📁 다운로드하고 싶은 폴더 (S3 내 경로)
prefix = ''  # 빈 문자열로 설정하면 버킷 전체에서 객체를 나열함
#prefix = 'example/'  # 'example/' 안에 있는 모든 파일 다운로드

# 💾 로컬에 저장할 디렉토리
# linux 버전으로 변경해야함
#local_download_root = '/opt/ncb'  # 원하는 로컬 경로로 변경하세요
local_download_root = 'D:\Code'  # 원하는 로컬 경로로 변경하세요

# S3에서 해당 prefix 아래의 파일들 가져오기
def dataDownload(bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('/'):  # 디렉터리라면 생략
                continue

            # 로컬 저장 경로 구성
            local_path = os.path.join(local_download_root, key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            print(f'Downloading s3://{bucket_name}/{key} -> {local_path}')
            s3.download_file(bucket_name, key, local_path)

    print("✅ All files downloaded.")
