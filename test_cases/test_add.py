import unittest
from library.ddt import data, ddt
from common.read_excel import ReadExcel
import os
from common.contents import DATA_DIR
from common.my_config import my_conf
from common.hand_data_re import replace_data, TestData
from common.hand_mysql import HandMysql
from common.hand_requests import HandRequests
import jsonpath
from common.my_logger import my_log


@ddt
class TestAdd(unittest.TestCase):
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "add")
    cases = excel.read_data()

    http = HandRequests()
    mysql = HandMysql()

    @data(*cases)
    def test_add(self, case):
        # 1、准备测试数据
        url = my_conf.get_str("env", "url") + case["url"]
        method = case["method"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(my_conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")

        expected = eval(case["expected"])

        row = case["case_id"] + 1

        if case["check_sql"]:
            # 获取该用户加标前的项目数
            sql = replace_data(case["check_sql"])
            self.old_count = self.mysql.count(sql)
        # 2、发送请求
        response = self.http.send(url=url,
                                  method=method,
                                  json=data,
                                  headers=headers)

        result = response.json()
        if case["interface"] == "login":
            admin_member_id = jsonpath.jsonpath(result, "$..id")[0]
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token

            setattr(TestData, "admin_member_id", admin_member_id)
            setattr(TestData, "token_data", token_data)

        print("实际结果：{}".format(result))
        print("预期结果：{}".format(expected))

        # 3、断言：比对结果
        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])

            if case["interface"] == "add" and result["code"] == 0 and result["msg"] == "OK":
                # 获取加标后的项目数量
                sql = replace_data(case["check_sql"])
                self.new_count = self.mysql.count(sql)
                self.assertEqual(self.old_count + 1, self.new_count)
                my_log.info("加标前的项目数量：{}\n加标后的项目数量：{}".format(self.old_count, self.new_count))

        except AssertionError as e:
            my_log.info("测试用例：{}-->>>执行不通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="不通过")

            raise e
        else:
            my_log.info("测试用例：{}-->>>执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
