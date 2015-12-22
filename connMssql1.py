# -*- coding: UTF-8 -*-

# import:
import pymssql

server = r'10.0.4.131\sqlserver2'
user = r'sa'
password = r'qwe123!@#'
database = r'master'


conn = pymssql.connect(server = server, user = user, password = password,database = database,charset="utf8")
cursor = conn.cursor()
cursor.execute("SELECT [pk],[c1] FROM [Test].[dbo].[T2]")
resList = cursor.fetchall()
print resList
#cursor.executemany(
#"INSERT INTO T2 VALUES (%d, %d)",[(1, 1)])

conn.commit()
conn.close()