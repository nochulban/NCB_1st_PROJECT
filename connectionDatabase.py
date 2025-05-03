import pymysql

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
    cursor = connectionDataBase() 
    query = """SELECT bucket_url FROM buckets_test"""
    cursor.execute(query)

    return cursor.fetchall()


#bucketAllSelect
def bucketTableAllSearch():
    cursor = connectionDataBase() 
    query = """SELECT * FROM buckets_test"""
    cursor.execute(query)

    return cursor.fetchall()

#repeatCheck
def repeatCheck(httpsName):
    cursor = connectionDataBase() 
    query = """SELECT COUNT(*) AS cnt FROM project_ncb.buckets_test WHERE bucket_url = %s"""
    cursor.execute(query, (httpsName,))
    duplicate_count = cursor.fetchone()
    #print(type(duplicate_count))
    #print(duplicate_count['cnt'])

    return int(duplicate_count['cnt'])



#INSERT


#documentTable
#SELECT


#INSERT


def insertDocuments(data):
    query = """INSERT INTO documents (file_name, url, extension, hash, date, bucket_url,file_size) 
VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor = connectionDataBase()
    cursor.execute(query, data)
