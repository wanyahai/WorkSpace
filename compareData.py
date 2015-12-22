# -*- coding: UTF-8 -*-
# compare data from different database

# import:
import pymssql

class MSSQL:
    """
    对pymssql的简单封装
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启

    用法：

    """

    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(server=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

server = r'10.0.4.131\sqlserver2'
user = r'sa'
password = r'qwe123!@#'
database = r'master'
sql_body ="""
SELECT [tax_id], [tax_name]
FROM [AlonsDW].[dbo].[tblTAX_RATES]
UNION ALL
SELECT [tax_id], [tax_name]
FROM [AlonsVH].[dbo].[tblTAX_RATES]
            """
sql = []
def main():
## ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
## #返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
## ms.ExecNonQuery("insert into WeiBoUser values('2','3')")

    ms = MSSQL(host=server,user=user,pwd=password,db=database)
    resList = ms.ExecQuery(sql_body)
    for (tax_id,tax_name) in resList:
        print tax_name

def get_tax(*args):

    sql_body = "SELECT [tax_id], [tax_name],[tax_rate] " \
               "FROM "
    for i in range(len(args)):
        sql.append(sql_body + str(args[i]) + ".[dbo].[tblTAX_RATES]")
    #print sql
    #print "\nINTERSECT\n".join(sql)
    ms = MSSQL(host=server,user=user,pwd=password,db=database)
    # 获取交集，每家商店共有的属性
    print r'Base Line information:'
    resList = ms.ExecQuery("\nINTERSECT\n".join(sql))
    for (tax_id,tax_name,tax_rate) in resList:
        print tax_id,tax_name,tax_rate

    for i in range(len(sql)):
        print "Special information about:" + args[i]
        relList1 = ms.ExecQuery(sql[i])
        relList2 = list(set(relList1) - set(resList))
        #print relList2
        for (tax_id,tax_name,tax_rate) in relList2:
            print tax_id,tax_name,tax_rate


#main()
get_tax("[AlonsDW]","[AlonsVH]","[CowgirlsA1]")
#if __name__ == '__main__':
#    main()