import logging
from common.my_config import my_conf
from common.contents import LOG_DIR
import os


class MyLogger:

    @staticmethod
    def crate_logger():
        # 1、创建一个名为python123的日志收集器
        my_log = logging.getLogger("python123")
        # 2、设置日志收集器的等级
        my_log.setLevel(my_conf.get_str("logging", "level"))

        # 3、添加输出渠道
        # 3.1、创建一个输出到控制台的输出渠道
        sh = logging.StreamHandler()
        # 3.2、设置输出等级
        sh.setLevel(my_conf.get_str("logging", "s_level"))
        # 3.3、将输出渠道绑定到日志收集器上
        my_log.addHandler(sh)

        # 4、添加输出渠道（输出到文件）
        # 4.1、创建一个输出到控制台的输出渠道
        # fh = logging.FileHandler("log.log", encoding="utf8")
        fh = logging.FileHandler(os.path.join(LOG_DIR,
                                              my_conf.get_str("logging", "file_name")),
                                 encoding="utf8")
        # 4.2、设置输出等级
        fh.setLevel(my_conf.get_str("logging", "f_level"))
        #  4.3、将输出渠道绑定到日志收集器上
        my_log.addHandler(fh)
        # 5、设置日志输出的格式
        # 5.1、创建一个日志输出格式
        formatter = logging.Formatter("%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s")
        # 5.2、将输出格式和输出渠道进行绑定
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return my_log


# 调用类的静态方法，创建一个日志收集器
my_log = MyLogger.crate_logger()
