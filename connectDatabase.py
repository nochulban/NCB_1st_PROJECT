import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

#DB 연결 
load_dotenv()

conn = pymysql.connect(
    host = os.getenv('HOST'),          # 👉 MySQL 서버 주소
    user = os.getenv('USER'),                # 👉 MySQL 사용자명
    password =os.getenv('PASSWORD'),  # 👉 MySQL 비밀번호
    database =os.getenv('DATABASE'),   # 👉 사용할 DB명
    charset='utf8mb4',
    autocommit=True
)



#bucketTable 
#SELECT

#bucketurlSelect
def getBucketUrl():
    try:
        cus = conn.cursor() 
        query = """SELECT bucket_url FROM buckets"""
        cus.execute(query)
    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()


#bucketAllSelect
def bucketTableAllSearch():
    try:
        cus = conn.cursor()
        query = """SELECT * FROM buckets"""
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()


#repeatCheck
def repeatCheck(httpsName):
    try:    
        cus = conn.cursor() 
        query = """SELECT COUNT(*) AS cnt FROM project_ncb.buckets WHERE bucket_url = %s"""
        cus.execute(query, (httpsName,))
        duplicate_count = cus.fetchone() 
        print(type(duplicate_count))       
        #print(duplicate_count['cnt'])
        countType = ("dict" if str(type(duplicate_count)) == "<class dict>" else "tuple" )

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    if countType == "dict":
        return int(duplicate_count['cnt'])
        #linux dict
    else:
        return int(duplicate_count[0])
        #window Tuple    

#TRUNCATE
def truncateBucketTable():
    try:
        cus = conn.cursor()
        query = f"TRUNCATE TABLE `buckets`;"
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()



#INSERT
def bucketUrlInsert(statusCode, count, httpsName):

    if statusCode == 200:
        try:
            cus = conn.cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '정상', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cus.execute(query, data)
            conn.commit()
            print("연결 O")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)        
    else:
        try:    
            cus = conn.cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '에러', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cus.execute(query, data)
            conn.commit()
            print("연결 X")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)    




#documentTable
#SELECT
def getDistinctBucketUrl():
    try:
        cus = conn.cursor()
        query = """SELECT DISTINCT bucket_url FROM documents"""
        cus.execute(query)
        return cus.fetchall()
    except pymysql.MySQLError as e:
        print("에러 발생:", e)
        return []



#INSERT
def insertDocuments(data):
    query = """INSERT INTO documents (file_name, url, extension, hash, date, bucket_url,file_size) 
VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cus = conn.cursor()
    cus.execute(query, data)

def fileRepeatCheck(httpsName):
    try:    
        cus = conn.cursor() 
        query = """SELECT COUNT(*) AS cnt FROM project_ncb.document WHERE bucket_url = %s"""
        cus.execute(query, (httpsName,))
        duplicate_count = cus.fetchone() 
        print(type(duplicate_count))       
        #print(duplicate_count['cnt'])
        countType = ("dict" if str(type(duplicate_count)) == "<class dict>" else "tuple" )

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    if countType == "dict":
        return int(duplicate_count['cnt'])
        #linux dict
    else:
        return int(duplicate_count[0])
        #window Tuple    

def truncateDocumentsTable():
    try:
        cus = conn.cursor()
        query = f"TRUNCATE TABLE `documents`;"
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()



def updateFileHash(bucket_url, file_hash):
    try:
        cus = conn.cursor()
        query = """
            UPDATE documents
            SET hash = %s
            WHERE bucket_url = %s
            """
        cus.execute(query, (file_hash, bucket_url))
        cus.commit()
        print(f"✅ Updated hash for {bucket_url}")
    except pymysql.MySQLError as e:
        print("에러 발생:", e)
    finally:
        cus.close()



#Report생성 쿼리
def setDataFrame():
    try:    
        cus = conn.cursor(pymysql.cursors.DictCursor)
        query = """SELECT 
    bucket_url,
    extension,
    date_format(date, '%Y-%m-%d') as dt,
    COUNT(*) AS file_count    
FROM 
   documents
WHERE
    bucket_url IS NOT NULL
GROUP BY 
    bucket_url, 
    extension,
    date_format(date, '%Y-%m-%d')
ORDER BY 
    bucket_url, 
    extension;"""
        cus.execute(query)
        rows = cus.fetchall()

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return rows


