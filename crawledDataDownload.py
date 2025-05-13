import boto3
import os
import connectDatabase
import hashlib
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__))) #경로 최소화 시 필요

# .env 파일 로드 (AWS 자격 증명 불러오기)
load_dotenv()

# 환경 변수에서 자격 증명 가져오기
# S3 클라이언트 생성
s3 = boto3.client(
    's3',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME")
)

# 🪣 버킷 이름: https://jaeyoon-example.s3-ap-northeast-2.amazonaws.com/

#bucket_name = bucket_url.split('//')[1].split('/')[0].split('.')[0]
#bucket_name = 'jaeyoon-example'
#bucket_name = 'photoism-apse-cms-prd'

# 📁 다운로드하고 싶은 폴더 (S3 내 경로)
prefix = ''  # 빈 문자열로 설정하면 버킷 전체에서 객체를 나열함
#prefix = 'example/'  # 'example/' 안에 있는 모든 파일 다운로드

# 💾 로컬에 저장할 디렉토리
# linux 버전으로 변경해야함
local_download_root = '/opt/test'  # 원하는 로컬 경로로 변경하세요
#local_download_root = 'D:\Code'  # 원하는 로컬 경로로 변경하세요

# S3에서 해당 prefix 아래의 파일들 가져오기
def dataDownload(url, bucket_name):
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
            fileHash = get_file_hash(local_path)
            connectDatabase.updateFileHash(url, fileHash)

    print(f"✅ All files downloaded from bucket: {bucket_name}")

def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    bucket_urls =connectDatabase.getDistinctBucketUrl()
    for url_tuple in bucket_urls:
        url = url_tuple[0]
        bucket_name = url.split('//')[1].split('/')[0].split('.')[0]
        if bucket_name:
            print(f"📦 Processing bucket: {bucket_name}")
            dataDownload(url, bucket_name)
            
        else:
            print(f"❌ Invalid bucket URL: {url}")
