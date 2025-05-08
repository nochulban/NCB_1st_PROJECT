import pandas as pd
import requests
import pymysql
import connectDatabase
from fpdf import FPDF
import os
from datetime import datetime

api_key = ""   # 👉 OpenAI API 키 입력
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ------------------ GPT로 개요+요약 생성 ------------------

def get_summary_from_gpt(keyword, data_sample, key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    prompt = (
    "당신은 클라우드 보안 탐지 보고서를 작성하는 AI입니다.\n"
        "이 보고서는 공개된 오브젝트 스토리지(S3/NCP 등)에서 수집한 문서들의 메타데이터를 기반으로 자동 생성됩니다.\n"
        "아래 샘플 데이터는 URL, 확장자, 수집일, 소속 버킷 등으로 구성된 메타데이터입니다.\n"
        "\n"
        "다음 형식으로 보고서를 작성하십시오. 형식은 마크다운이 아닌 **텍스트 기반(plain text)**입니다.\n"
        "\n"
        "==============================\n"
        "공개 S3 버킷 대상 유출 의심 문서 리스트 보고서\n"
        "==============================\n"
        "\n"
        "[보고서 개요]\n"
        f"검색 키워드 '{keyword}'를 기반으로 자동화된 보안 점검 시스템을 통해 공개 오브젝트 스토리지 내에서 수집된 유출 의심 파일들을 분석하였습니다. 본 보고서는 수집 대상의 기본 정보, 수집 방식, 탐지 결과를 포함합니다.\n"
        "\n"
        "[탐지 요약]\n"
        "- 총 탐지 수: (자동 계산)\n"
        "- 고유 문서 수: (자동 계산)\n"
        "- 공개 버킷 수: (자동 계산)\n"
        "\n"
        "[유출 문서 상세 리스트]\n"
        "각 항목은 한 줄씩 구분하여 다음 형식으로 나열:\n"
        "  URL: {bucket_url}\n"
        "  파일수: {file_count}\n"
        "  수집일: {dt}\n"
        "\n"
        "[결론 및 권고사항]\n"
        "탐지된 문서들은 외부에 민감 정보가 노출되었을 가능성이 있으며, 즉각적인 접근 제어 및 내부 보안 점검이 요구됩니다. 보안 담당자에게 다음과 같은 조치를 권고합니다:\n"
        "- 공개 버킷 설정 여부 검토 및 비공개 전환\n"
        "- 문서 내 포함된 정보의 민감도 확인\n"
        "- 자동 점검 시스템의 정기 실행 도입\n"
        "\n"
        #"※ 이 보고서는 Python 기반 자동화 도구에 의해 PDF로 출력됩니다. 항목 간 간격 및 줄바꿈을 고려해 출력되도록 구성해 주세요.\n"
        "\n"
        f"샘플 데이터:\n{data_sample}"
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 2048
    }

    response = requests.post(url, headers=headers, json=data, timeout=200)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']

# ------------------ MySQL 연결 및 데이터 가져오기 ------------------

def load_mysql_table_to_dataframe():

    rows = connectDatabase.setDataFrame()
    df = pd.DataFrame(rows)
    return df

# ------------------ PDF 보고서 저장 ------------------

def save_report_to_pdf(pdf_path, summary_text, df):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font("NanumGothic", '', "NanumGothic.ttf", uni=True)
    pdf.set_font("NanumGothic", size=14)

    # 개요 및 탐지 요약
    pdf.multi_cell(0, 10, "1. 보고서 개요 및 탐지 요약")
    pdf.set_font("NanumGothic", size=12)
    for line in summary_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    # 유출 문서 리스트
    # pdf.ln(5)
    # pdf.set_font("NanumGothic", size=14)
    # pdf.multi_cell(0, 10, "2. 유출 문서 리스트")
    # pdf.set_font("NanumGothic", size=12)

    if 'file_name' in df.columns and 'bucket_url' in df.columns:
        bucket_count = df['bucket_url'].nunique()
        file_count = df[''].nunique()
        pdf.multi_cell(0, 10, f"탐지된 전체 버킷 수: {bucket_count}개")
        pdf.multi_cell(0, 10, f"탐지된 전체 파일 수: {file_count}개")
        pdf.ln(5)

        grouped = df.groupby('bucket_url')
        for bucket, group in grouped:
            pdf.ln(4)
            pdf.set_font("NanumGothic", size=12)
            pdf.multi_cell(0, 8, f"[버킷 주소] {bucket}")
            for idx, row in group.iterrows():
                filename = str(row.get('file_name', '파일명 없음'))
                #extension = str(row.get('extension', '확장자 없음'))
                file_count = str(row.get('file_count', '확장자 없음'))
                #file_size = str(row.get('file_size', '크기 정보 없음'))
                pdf.multi_cell(0, 8, f"- {filename}, {file_count} ")
    else:
        print("파일명 또는 버킷 주소 정보 없음")

    pdf.output(pdf_path, "F")

# ------------------ 전체 파이프라인 실행 ------------------

def run_pipeline(keyword):
    df = load_mysql_table_to_dataframe()

    sample = df.head(5).to_string(index=False)
    print(df)

    summary_text = get_summary_from_gpt(keyword, df, api_key)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = f"output/report_{timestamp}.pdf"

    save_report_to_pdf(pdf_path, summary_text, df)
    print(f"✅ PDF 보고서가 생성되었습니다: {pdf_path}")

    #connectDatabase.truncateBucketTable()
    #connectDatabase.truncateDocumentsTable()

# ------------------ 메인 실행 ------------------

#if __name__ == "__main__":
    
    ## 저장할 파일 경로 설정
    ##ppt_save_path = "bucket_report.pptx"
    ##docx_save_path = "bucket_report.docx"    

    # 테스트시 주석 해제 
    # keyword = input()
    # run_pipeline(keyword)
