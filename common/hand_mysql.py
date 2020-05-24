import pymysql
from common.my_config import my_conf


class HandMysql:
    def __init__(self):
        # 连接到数据库
        self.con = pymysql.connect(host=my_conf.get_str("mysql", "host"),
                                   user=my_conf.get_str("mysql", "user"),
                                   password=my_conf.get_str("mysql", "password"),
                                   port=my_conf.get_int("mysql", "port"),
                                   charset="utf8")
        # 创建一个游标
        self.cur = self.con.cursor()

    def get_one(self, sql):
        """获取查询到的第一条数据"""
        self.con.commit()  # 提交操作，保证当前数据库数据时最新的
        self.cur.execute(sql)
        return self.cur.fetchone()

    def get_all(self, sql):
        """获取查询到的所有数据"""
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def count(self, sql):
        """返回查找到的数据条数"""
        self.con.commit()
        return self.cur.execute(sql)

    def close(self):
        # 关闭游标对象
        self.cur.close()
        # 断开数据库连接
        self.con.close()


if __name__ == '__main__':
    mysql = HandMysql()
    sql = "select * from futureloan.member where mobile_phone = '15223817776';"
    res = mysql.get_one(sql)
    print(res)
