import unittest
from common.read_excel import ReadExcel
from common.contents import DATA_DIR
import os
from library.ddt import data, ddt
from common.hand_requests import HandRequests
from common.my_config import my_conf
from common.my_logger import my_log


@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(os.path.join(DATA_DIR, "apicases_login.xlsx"), "login")
    cases = excel.read_data()

    http = HandRequests()

    @data(*cases)
    def test_login(self, case):
        # 1、准备测试用例
        # 拼接完整的url
        url = my_conf.get_str("env", "url") + case["url"]
        # 请求方法
        method = case["method"]
        # 请求参数
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

        print("实际结果：{}".format(result))
        print("预期结果：{}".format(expected))

        # 3、断言：比对预期结果和实际结果
        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="不通过")
            my_log.info("用例：{}--->执行未通过".format(case["title"]))
            print("实际结果为：{}".format(result))
            print("预期结果为：{}".format(expected))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例：{}--->执行通过".format(case["title"]))
