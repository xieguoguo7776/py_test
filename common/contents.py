"""该模块用来处理整个项目目录的路径"""

import os

# 获取当前文件的绝对路径获取(下面方法在服务器上无法获取绝对路径使用这个方法)
dir = os.path.abspath(__file__)

# 项目目录的路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 配置文件的路径
CONF_DIR = os.path.join(BASE_DIR, "conf")
# 用来数据的路径
DATA_DIR = os.path.join(BASE_DIR, "data")
# 日志文件的路径
LOG_DIR = os.path.join(BASE_DIR, "log")
# 测试报告的路径
REPORT_DIR = os.path.join(BASE_DIR, "report")
# 测试用例模块所在的路径
CASE_DIR = os.path.join(BASE_DIR, "test_cases")
