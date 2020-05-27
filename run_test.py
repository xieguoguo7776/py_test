import unittest
from common.contents import REPORT_DIR, CASE_DIR
from common.my_config import my_conf
import os

from common.send_email import send_msg

# 第一步：创建一个测试套件
suite = unittest.TestSuite()

# 第二步：将测试用例，加载到测试套件中(通过路径加载)
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))
# suite.addTest(loader.loadTestsFromModule(test_login))

# 第三步：创建一个测试运行程序启动器
from HTMLTestRunnerNew import HTMLTestRunner

report_path = os.path.join(REPORT_DIR, my_conf.get_str("report", "file_name"))
with open(report_path, "wb") as f:
    runner = HTMLTestRunner(stream=f,
                            title="测试报告",
                            description="测试报告的描述信息",
                            tester="小倩倩")

    runner.run(suite)

# 执行完代码之后，发送邮件
send_msg(report_path)
