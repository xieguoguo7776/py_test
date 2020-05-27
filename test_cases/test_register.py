import unittest
from common.read_excel import ReadExcel
from common.contents import DATA_DIR
import os
from library.ddt import data, ddt
from common.hand_requests import HandRequests
from common.my_config import my_conf
from common.my_logger import my_log
import random
from common.hand_mysql import HandMysql


@ddt
class TestRegister(unittest.TestCase):
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "register")
    cases = excel.read_data()

    http = HandRequests()
    mysql = HandMysql()

    @data(*cases)
    def test_register(self, case):
        # 1、准备测试用例
        # 拼接完整的url
        url = my_conf.get_str("env", "url") + case["url"]
        # 请求方法
        method = case["method"]
        # 请求参数
        # 判断是否有手机号码需要替换
        if "#phone#" in case["data"]:
            # 生成一个手机号码
            self.phone = self.random_phone()
            # 进行替换
            case["data"] = case["data"].replace("#phone#", self.phone)
        data = eval(case["data"])
        # 请求头
        headers = eval(my_conf.get_str("env", "headers"))
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单中的行（用于测试结果回写）
        row = case["case_id"] + 1

        # 2、发送请求到接口，获取时间结果
        response = self.http.send(url=url,
                                  method=method,
                                  json=data,
                                  headers=headers)
        # 获取实际结果
        result = response.json()
        print("实际结果为：{}".format(result))
        print("预期结果为：{}".format(expected))

        # 3、断言：比对预期结果和实际结果
        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])

            # 判断注册成功，去数据库查询当前注册成功的账号是否存在
            if result["msg"] == "OK":
                sql = "select * from futureloan.member where mobile_phone = '{}';".format(self.phone)
                # 获取数据库中有没有该用户的信息
                count = self.mysql.count(sql)
                self.assertEqual(count, 1)
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="不通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))

    # # ------------------------------手机号码未数据库验证代码------------------------------
    # @staticmethod
    # def random_phone():
    #     """生成随机的手机号码"""
    #     phone = "152"
    #     for i in range(8):
    #         phone += str(random.randint(0, 9))
    #     return phone

    # ------------------------------手机号码数据库验证代码------------------------------
    @classmethod
    def random_phone(cls):
        """生成随机的手机号码"""
        while True:
            phone = "152"
            for i in range(8):
                phone += str(random.randint(0, 9))
            # 去数据库查询，看数据库该手机号是否已注册
            count = cls.mysql.count("select * from futureloan.member where mobile_phone={}".format(phone))
            if count == 0:
                return phone

    @classmethod
    def tearDownClass(cls) -> None:
        # 关闭数据库的连接
        cls.mysql.close()
