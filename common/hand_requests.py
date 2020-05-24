"""
封装的目的：
封装的需求：
    发送post请求、get请求、patch请求
    如何做到不同请求方式的接口去发送不同的请求
    解决办法--加判断：if

"""

import requests
import jsonpath


class HandRequests:

    def send(self, url, method, headers=None, params=None, json=None, data=None):
        """
        发送http请求（满足表单、json方式传参）
        :param url: 请求地址
        :param method: 请求方法
        :param headers: 请求头：传参格式为json，传默认值是因为项目可能不用传请求头
        :param params:  请求参数：传参格式为json，传默认值是因为非get请求用不到
        :param json:  请求参数：传参格式j为son，传默认值是因为非post、patch请求用不到
        :param data:  请求参数：传参格式为表单（x-www-form-urlencoded）时使用
        :return:
        """
        # 将请求的方法转化成小写
        method = method.lower()
        if method == "post":
            return requests.post(url=url, json=json, data=data, headers=headers)
        elif method == "patch":
            return requests.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return requests.get(url=url, params=params, data=data, headers=headers)
        # 项目中还需要其他请求方式，在此续加判断即可


class HandSessionRequests:
    """使用session鉴权的接口，使用这个类来发送请求"""

    def __init__(self):
        self.se = requests.session()

    def send(self, url, method, headers=None, params=None, json=None, data=None):
        """
        发送http请求（满足表单、json方式传参）
        :param url: 请求地址
        :param method: 请求方法
        :param headers: 请求头：传参格式为json，传默认值是因为项目可能不用传请求头
        :param params:  请求参数：传参格式为json，传默认值是因为非get请求用不到
        :param json:  请求参数：传参格式j为son，传默认值是因为非post、patch请求用不到
        :param data:  请求参数：传参格式为表单（x-www-form-urlencoded）时使用
        :return:
        """
        # 将请求的方法转化成小写
        method = method.lower()
        if method == "post":
            return self.se.post(url=url, json=json, data=data, headers=headers)
        elif method == "patch":
            return self.se.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return self.se.get(url=url, params=params, data=data, headers=headers)
        # 项目中还需要其他请求方式，在此续加判断即可


if __name__ == '__main__':
    # ------------------------------登录------------------------------
    # 登录的请求地址
    login_url = "http://api.lemonban.com/futureloan/member/login"
    # 登录的请求参数
    login_data = {"mobile_phone": "15223817776",
                  "pwd": "12345689"
                  }
    # 登录的请求头
    headers = {"X-Lemonban-Media-Type": "lemonban.v2",
               "Content-Type": "application/json"}
    # 发送登录的请求
    http = HandRequests()
    response = http.send(url=login_url,
                         json=login_data,
                         headers=headers,
                         method="POST")
    # 获取返回的json数据
    json_data = response.json()
    print(json_data)
