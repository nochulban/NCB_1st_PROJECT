import requests
import hashlib
import os
import connectDatabase

API_KEY = os.getenv('VIRUSTOTAL_API')
FILE_PATH = 'food.txt'

# SHA-256 해시 계산
def get_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# 해시 기반 분석 결과 조회
def get_report_by_hash(file_url, file_name, file_hash, extension):
    isNormal = True        
    url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
    headers = {
        'x-apikey': API_KEY,
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data['data']['attributes']['last_analysis_stats']
        malicious = stats['malicious']
        suspicious = stats['suspicious']
        harmless = stats['harmless']
        undetected = stats['undetected']

        print(f"[+] 해시 분석 결과")
        print(f"  - Malicious : {malicious}")
        print(f"  - Suspicious: {suspicious}")
        print(f"  - Harmless  : {harmless}")
        print(f"  - Undetected: {undetected}")

        if malicious > 0 or suspicious > 0:
            isNormal = False
            print("⚠️  이 파일은 악성일 수 있습니다.")
            connectDatabase.classificationFile(isNormal, file_url, file_name ,file_hash, extension, malicious, suspicious )
        else:
            print("✅ 이 파일은 안전해 보입니다.")
            connectDatabase.classificationFile(isNormal, file_url, file_name ,file_hash, extension,0 ,0)
    elif response.status_code == 404:
        print("❌ 해당 파일 해시는 VirusTotal에 존재하지 않습니다. 파일을 직접 업로드해야 합니다.")
        connectDatabase.classificationFile(isNormal, file_url, file_name ,file_hash, extension,0, 0)
    else:
        print("[!] 해시 조회 실패:", response.text)


def scan_all_files_in_directory(directory):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file == '.DS_Store':
                pass
            file_path = os.path.join(root, file)
            try:                
                if count == 10:
                    print('10회차 횟주 제한 종료')
                    break
                url = root.split('ncb/')[1]
                extension = file.split('.')[1]
                file_hash = get_file_hash(file_path)
                get_report_by_hash(url, file, file_hash,extension)
                count+=1
            except Exception as e:
                print(f"[!] 파일 처리 중 오류 발생: {file_path} - {str(e)}")


# if __name__ == '__main__':
# #     #file_hash = get_file_hash(FILE_PATH)
# #     #file_hash = '6fd8531c552f86e99908e8ad5144074add2bfc71d660282fce077a2de90cde79'
# #     #print(f"[+] SHA-256 해시: {file_hash}")
# #     #get_report_by_hash(file_hash)2

#     TARGET_DIR = '/Users/leejaeyoon/ncb'
#     #extract_all_subfolders(TARGET_DIR)
#     scan_all_files_in_directory(TARGET_DIR)

