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
def bucketUrlSearch():
    try:
        cursor = connectionDataBase().cursor() 
        query = """SELECT bucket_url FROM buckets_test"""
        cursor.execute(query)
    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()


#bucketAllSelect
def bucketTableAllSearch():
    try:
        cursor = connectionDataBase().cursor()
        query = """SELECT * FROM buckets_test"""
        cursor.execute(query)

    except pymysql.MySQLError as e:
        print("에러 발생:", e)

    return cursor.fetchall()


#repeatCheck
def repeatCheck(httpsName):
    try:    
        cursor = connectionDataBase().cursor() 
        query = """SELECT COUNT(*) AS cnt FROM project_ncb.buckets_test WHERE bucket_url = %s"""
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



#INSERT
def bucketUrlInsert(statusCode, count, httpsName):

    if statusCode == 200:
        try:
            cursor = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets_test (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (statusCode, '정상', datetime.now().strftime('%Y.%m.%d - %H:%M:%S'),'grayhat', count, httpsName )
            cursor.execute(query, data)
            connectionDataBase().commit()
            print("연결 O")
        except pymysql.MySQLError as e:
            print("에러 발생:", e)        
    else:
        try:    
            cursor = connectionDataBase().cursor()
            query = """INSERT INTO project_ncb.buckets_test (status_code, connection_state, collected_at, source, file_count, bucket_url)VALUES (%s, %s, %s, %s, %s, %s)"""
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
