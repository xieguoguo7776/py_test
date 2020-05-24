import re
from common.my_config import my_conf


class TestData:
    """这个类的作用：专门用来保存一些要替换的数据"""
    pass


def replace_data(data):
    r = "#(.+?)#"
    # 判断是否有需要替换的数据（while后面为True就一直循环）
    while re.search(r, data):
        # 匹配出第一个要替换的数据
        res = re.search(r, data)
        # 提取待替换的内容
        item = res.group()
        # 获取替换内容中的数据项
        key = res.group(1)
        try:
            # 根据替换内容中的数据项去配置文件中找到对应的内容，进行替换
            data = data.replace(item, str(my_conf.get_str("test_data", key)))
        except:
            # 没有在配置文件找到对应的内容，就去TestData类中去找
            data = data.replace(item, str(getattr(TestData, key)))

    # 返回替换好的数据
    return data


# # 通过读取配置文件替换
# data = '{"mobile_phone":"#phone#","pwd":"#pwd#","user":"#user#"}'
# data = replace_data(data)
# print(data)

# # 问题--配置文件没有对应的内容？
# # 解决办法--去获取临时变量（TestData类里面）
# data = '{"member_id": #member_id#,"amount":600}'
# data = replace_data(data)
# print(data)
