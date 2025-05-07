import pymysql
from datetime import datetime

#DB 연결 
def connectionDataBase():
    conn = None
    conn = pymysql.connect(
        host = '',          # 👉 MySQL 서버 주소
        user = '',                # 👉 MySQL 사용자명
        password ='',  # 👉 MySQL 비밀번호
        database = '',   # 👉 사용할 DB명
        charset='',
        autocommit=True
    )

    return conn.cursor()

#bucketTable 
#SELECT

#bucketurlSelect
def getBucketUrl():
    try:
        cursor = connectionDataBase().cursor() 
        query = """SELECT bucket_url FROM buckets"""
        cursor.execute(query)
    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()


#bucketAllSelect
def bucketTableAllSearch():
    try:
        cursor = connectionDataBase().cursor()
        query = """SELECT * FROM buckets"""
        cursor.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()


#repeatCheck
def repeatCheck(httpsName):
    try:    
        cursor = connectionDataBase().cursor() 
        query = """SELECT COUNT(*) AS cnt FROM project_ncb.buckets WHERE bucket_url = %s"""
        cursor.execute(query, (httpsName,))
        duplicate_count = cursor.fetchone() 
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
        cursor = connectionDataBase().cursor()
        query = f"TRUNCATE TABLE `buckets`;"
        cursor.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()



#INSERT
def bucketUrlInsert(statusCode, count, httpsName):

    if statusCode == 200:
        try:
            cursor = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '정상', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cursor.execute(query, data)
            connectionDataBase().commit()
            print("연결 O")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)        
    else:
        try:    
            cursor = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '에러', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cursor.execute(query, data)
            connectionDataBase().commit()
            print("연결 X")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)    




#documentTable
#SELECT


#INSERT
def insertDocuments(data):
    query = """INSERT INTO documents (file_name, url, extension, hash, date, bucket_url,file_size) 
VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor = connectionDataBase().cursor()
    cursor.execute(query, data)

def fileRepeatCheck(httpsName):
    try:    
        cursor = connectionDataBase().cursor() 
        query = """SELECT COUNT(*) AS cnt FROM project_ncb.document WHERE bucket_url = %s"""
        cursor.execute(query, (httpsName,))
        duplicate_count = cursor.fetchone() 
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
        cursor = connectionDataBase().cursor()
        query = f"TRUNCATE TABLE `documents`;"
        cursor.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()



#Report생성 쿼리
def setDataFrame():
    try:    
        cursor = connectionDataBase().cursor(pymysql.cursors.DictCursor)
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
        cursor.execute(query)
        rows = cursor.fetchall()

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return rows
