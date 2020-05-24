import unittest
from common.read_excel import ReadExcel
import os
from library.ddt import data, ddt
from common.contents import DATA_DIR
from common.my_config import my_conf
from common.hand_data_re import replace_data, TestData
from common.hand_requests import HandRequests
import jsonpath
from common.my_logger import my_log
from common.hand_mysql import HandMysql
import decimal


@ddt
class TestInvest(unittest.TestCase):
    # 读取excel测试数据
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "invvv")
    cases = excel.read_data()

    # 初始化发送请求对象
    http = HandRequests()
    mysql = HandMysql()

    @classmethod
    def setUpClass(cls) -> None:
        # 管理员登录，准备数据
        url = my_conf.get_str("env", "url") + "/member/login"
        data = {"mobile_phone": my_conf.get_str("test_data", "admin_phone"),
                "pwd": my_conf.get_str("test_data", "admin_pwd")}
        method = "post"
        headers = eval(my_conf.get_str("env", "headers"))

        # 发送请求
        response = cls.http.send(url=url, method=method, json=data, headers=headers)

        # 获取登录返回的管理员用户id、token信息
        result = response.json()
        admin_member_id = jsonpath.jsonpath(result, "$..id")[0]
        token_type = jsonpath.jsonpath(result, "$..token_type")[0]
        token = jsonpath.jsonpath(result, "$..token")[0]
        admin_token_data = token_type + " " + token

        # 将管理员用户id、token信息设置在TestData类中（类属性），用于管理员加标
        setattr(TestData, "admin_member_id", admin_member_id)
        setattr(TestData, "admin_token_data", admin_token_data)

    def setUp(self) -> None:
        # 管理员加标(新增项目)，准备数据
        url = my_conf.get_str("env", "url") + "/loan/add"
        data = {"member_id": getattr(TestData, "admin_member_id"),
                "title": "借钱实现财富自由",
                "amount": 4000,
                "loan_rate": 12.0,
                "loan_term": 3,
                "loan_date_type": 1,
                "bidding_days": 5}
        method = "post"
        headers = eval(my_conf.get_str("env", "headers"))
        headers["Authorization"] = getattr(TestData, "admin_token_data")

        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)

        # 获取登录返回的管理员加标的标id
        result = response.json()
        loan_id = jsonpath.jsonpath(result, "$..id")[0]

        # 将管理员加标的标id设置在TestData类中（类属性），用于管理员审核
        setattr(TestData, "loan_id", loan_id)

        # 管理员审核项目，准备数据
        url = my_conf.get_str("env", "url") + "/loan/audit"
        data = {"loan_id": getattr(TestData, "loan_id"), "approved_or_not": "true"}
        method = "PATCH"
        headers = eval(my_conf.get_str("env", "headers"))
        headers["Authorization"] = getattr(TestData, "admin_token_data")

        # 发送请求
        self.http.send(url=url, method=method, json=data, headers=headers)

        # 用户登录，准备数据
        url = my_conf.get_str("env", "url") + "/member/login"
        data = {"mobile_phone": my_conf.get_str("test_data", "phone"),
                "pwd": my_conf.get_str("test_data", "pwd")}
        method = "post"
        headers = eval(my_conf.get_str("env", "headers"))

        # 发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)

        # 获取登录返回的用户id、token信息
        result = response.json()
        member_id = jsonpath.jsonpath(result, "$..id")[0]
        token_type = jsonpath.jsonpath(result, "$..token_type")[0]
        token = jsonpath.jsonpath(result, "$..token")[0]
        token_data = token_type + " " + token

        # 将用户id、token信息设置在TestData类中（类属性），用用户投资
        setattr(TestData, "member_id", member_id)
        setattr(TestData, "token_data", token_data)

    @data(*cases)
    def test_invest(self, case):
        # 1、测试数据
        url = my_conf.get_str("env", "url") + case["url"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        method = case["method"]
        headers = eval(my_conf.get_str("env", "headers"))
        headers["Authorization"] = getattr(TestData, "token_data")
        expected = eval(case["expected"])

        row = case["case_id"] + 1

        if case["check_sql"]:
            # 数据库校验，获取投资之前数据条数
            self.old_count = self.mysql.count(replace_data(case["check_sql"]))

        # 2、发送请求
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        result = response.json()

        print("实际结果：{}".format(result))
        print("预期结果：{}".format(expected))

        # 3、断言
        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
            if case["check_sql"]:
                # 数据库校验，获取投资之前数据条数
                new_count = self.mysql.count(replace_data(case["check_sql"]))
                my_log.info("投资之前条数：{}\n投资之后条数：{}".format(self.old_count, new_count))
                # 数据库校验，获取投资之后金额
                new_money = self.mysql.get_one(replace_data(case["check_sql"]))[0]
                # 获取投资金额（需要转换类型）
                invest_money = decimal.Decimal(data["amount"])
                my_log.info("投资金额：{}\n投资之后金额：{}".format(invest_money, new_money))
                self.assertEqual(new_money - invest_money, 0)
                self.assertEqual(self.old_count + 1, new_count)

        except AssertionError as e:
            my_log.info("测试用例：{}-->>>执行不通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="不通过")
            raise e
        else:
            my_log.info("测试用例：{}-->>>执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
