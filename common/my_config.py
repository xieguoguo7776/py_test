from configparser import ConfigParser
from common.contents import CONF_DIR
import os


class MyConf:

    def __init__(self, file_name, encoding="utf8"):
        self.file_name = file_name
        self.encoding = encoding
        # 创建一个文件解析对象，设置为对象的conf
        self.conf = ConfigParser()
        # 使用解析器对象，加载配置文件中的内容
        self.conf.read(file_name, encoding)

    def get_str(self, section, option):
        """
        读取字符串数据
        :param section:配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.get(section, option)

    def get_int(self, section, option):
        """
        读取数值数据
        :param section:配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getint(section, option)

    def get_float(self, section, option):
        """
        读取浮点数数据
        :param section:配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getfloat(section, option)

    def get_boolean(self, section, option):
        """
        读取布尔值数据
        :param section:配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        return self.conf.getboolean(section, option)

    def write_data(self, section, option, value):
        """
        写入数据
        :param section:配置块
        :param option: 配置项
        :param value: 写入配置项对应的值
        """
        self.conf.set(section, option, value)
        self.conf.write(open(self.file_name, "w", encoding=self.encoding))


class MyConf2(ConfigParser):
    """用继承的方式封装"""

    def __init__(self, file_name, encoding="utf8"):
        # 调用父类原来的init方法
        super().__init__()
        self.fine_name = file_name
        self.encoding = encoding
        self.read(file_name, encoding)

    def write_data(self, section, option, value):
        self.set(section, option, value)
        self.write(open(self.fine_name, "w", encoding=self.encoding))


# 获取配置文件的绝对路径
conf_path = os.path.join(CONF_DIR, "conf.ini")
# 创建一个文件解析对象(在这里创建可以直接调用)
my_conf = MyConf(conf_path)

if __name__ == '__main__':
    conf = MyConf("conf.ini")
    # 读取数据
    level = conf.get_str("logging", "level")
    print(level)
    # 写入数据
    conf.write_data("logging", "aaa", "123")
