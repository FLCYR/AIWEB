# insert data to mysql database
import os

import pymysql


db = pymysql.connect(
         host='127.0.0.1',
         port=3306,
         user='root',
         passwd='123456',
         db ='asserts',
         charset='utf8')



# 使用cursor()方法创建一个游标对象cursor
cursor = db.cursor()
# 使用execute()方法执行SQL查询
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print("Database version : %s " % data)



def insert_images():

    # list all images in the folder
    path = '../static/WallPapers'

    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            print(file)
            # insert data to database
            sql = f"insert into image(uri,name,height,width) values('{file}','{file}',100,100)"
            cursor.execute(sql)
            db.commit()
        else:
            print('not a jpg file')


if __name__ == '__main__':

    insert_images()
    db.close()