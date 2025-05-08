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
        cus = connectionDataBase().cursor() 
        query = """SELECT bucket_url FROM buckets"""
        cus.execute(query)
    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()


#bucketAllSelect
def bucketTableAllSearch():
    try:
        cus = connectionDataBase().cursor()
        query = """SELECT * FROM buckets"""
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()


#repeatCheck
def repeatCheck(httpsName):
    try:    
        cus = connectionDataBase().cursor() 
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
        cus = connectionDataBase().cursor()
        query = f"TRUNCATE TABLE `buckets`;"
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()



#INSERT
def bucketUrlInsert(statusCode, count, httpsName):

    if statusCode == 200:
        try:
            cus = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '정상', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cus.execute(query, data)
            connectionDataBase().commit()
            print("연결 O")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)        
    else:
        try:    
            cus = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '에러', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cus.execute(query, data)
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
    cus = connectionDataBase().cursor()
    cus.execute(query, data)

def fileRepeatCheck(httpsName):
    try:    
        cus = connectionDataBase().cursor() 
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
        cus = connectionDataBase().cursor()
        query = f"TRUNCATE TABLE `documents`;"
        cus.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cus.fetchall()



#Report생성 쿼리
def setDataFrame():
    try:    
        cus = connectionDataBase().cursor(pymysql.cursors.DictCursor)
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
