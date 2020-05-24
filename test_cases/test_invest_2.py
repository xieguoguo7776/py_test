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
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "invest")
    cases = excel.read_data()

    http = HandRequests()
    mysql = HandMysql()

    @data(*cases)
    def test_invest(self, case):
        url = my_conf.get_str("env", "url") + case["url"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        method = case["method"]
        headers = eval(my_conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
        expected = eval(case["expected"])

        row = case["case_id"] + 1

        # 获取用户投资之前余额
        if case["sql"]:
            self.s_money = self.mysql.get_one(replace_data(case["sql"]))[0]

        response = self.http.send(url=url, method=method, headers=headers, json=data)
        result = response.json()

        if case["interface"] == "login":
            member_id = jsonpath.jsonpath(result, "$..id")[0]
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token

            setattr(TestData, "member_id", member_id)
            setattr(TestData, "token_data", token_data)

        elif case["interface"] == "add":
            loan_id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "loan_id", loan_id)

        print("实际结果：{}".format(result))
        print("预期结果：{}".format(expected))

        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
            if case["check_sql"]:
                # 数据库校验，获取投资之后金额
                new_money = self.mysql.get_one(replace_data(case["check_sql"]))[0]
                # 获取投资金额（需要转换类型）
                self.invest_money = decimal.Decimal(data["amount"])
                my_log.info("项目投资金额：{}\n项目投资之后金额：{}".format(self.invest_money, new_money))
                # 断言项目余额=投资金额
                self.assertEqual(new_money - self.invest_money, 0)

            # 获取用户投资之后余额
            if case["sql"]:
                e_money = self.mysql.get_one(replace_data(case["sql"]))[0]
                my_log.info("用户投资之前余额：{}\n用户投资金额：{}\n用户投资之后余额：{}".format(self.s_money, self.invest_money, e_money))
                # 断言用户投资前余额-投资金额=投资后余额
                self.assertEqual(self.s_money - self.invest_money, e_money)

        except AssertionError as e:
            my_log.info("测试用例：{}-->>>执行不通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="不通过")
            raise e
        else:
            my_log.info("测试用例：{}-->>>执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
