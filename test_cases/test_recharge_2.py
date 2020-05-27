import unittest
from common.read_excel import ReadExcel
from common.contents import DATA_DIR
import os
from library.ddt import data, ddt
from common.hand_requests import HandRequests
from common.my_config import my_conf
from common.my_logger import my_log
import jsonpath
from common.hand_mysql import HandMysql
import decimal
from common.hand_data_re import replace_data, TestData


@ddt
class TestRecharge(unittest.TestCase):
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "recharge")
    cases = excel.read_data()

    http = HandRequests()
    mysql = HandMysql()

    @data(*cases)
    def test_recharge(self, case):
        # 1、准备测试用例
        # 拼接完整的url
        url = my_conf.get_str("env", "url") + case["url"]
        # 请求方法
        method = case["method"]
        # 请求参数
        case["data"] = replace_data(case["data"])

        data = eval(case["data"])
        # 请求头
        headers = eval(my_conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在表单中的行（用于测试结果回写）
        row = case["case_id"] + 1

        # 获取充值之前的金额
        if case["check_sql"]:
            sql = case["check_sql"].format(my_conf.get_str("test_data", "user"))
            self.old_money = self.mysql.get_one(sql)[0]
            print(self.old_money)

        # 2、发送请求到接口，获取时间结果
        response = self.http.send(url=url,
                                  method=method,
                                  json=data,
                                  headers=headers)
        # 获取实际结果
        result = response.json()
        print("实际结果为：{}".format(result))
        print("预期结果为：{}".format(expected))

        if case["interface"] == "login":
            # 将用户id和token值提取出来保存为类属性（通过类名.属性名）
            member_id = jsonpath.jsonpath(result, "$..id")[0]

            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token

            setattr(TestData, "member_id", member_id)
            setattr(TestData, "token_data", token_data)

        # 3、断言：比对预期结果和实际结果
        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])

            # 断言：充值之后的金额-充值金额=充值之前的金额（数据库金额是decimal类型的，需要将充值金额转换成decimal类型--先转换成字符串在转换）
            if case["interface"] != "login" and result["code"] == 0 and result["msg"] == "OK":
                # 获取充值金额
                recharge_money = decimal.Decimal(str(data["amount"]))
                # 获取充值之后的金额
                sql = case["check_sql"].format(my_conf.get_str("test_data", "user"))
                new_money = self.mysql.get_one(sql)[0]
                my_log.info("充值之前的金额：{}\n充值的金额：{}\n充值之后的金额：{}".format(self.old_money, recharge_money, new_money))
                # 断言
                self.assertEqual(new_money - recharge_money, self.old_money)

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="不通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mysql.close()
