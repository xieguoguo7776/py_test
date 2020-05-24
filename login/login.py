"""
"""


def login_check(username=None, password=None):
    """
    登录校验的函数
    :param username: 账号
    :param password:  密码
    :return: dict type
    """
    if all([username, password]):
        if username == 'python24' and password == 'lemonban':
            return {"code": 0, "msg": "登录成功"}
        else:
            return {"code": 1, "msg": "账号或密码不正确"}
    else:
        return {"code": 1, "mgs": "所有的参数不能为空"}


if __name__ == '__main__':
    # 第一条：账号密码都正确。
    # 预取结果
    expected = {"code": 0, "msg": "登录成功"}
    result = login_check("python24", "lemonban")
    print(result)
    if expected == result:
        print("用例执行通过")
    else:
        print("用例执行未通过")

    # 第二条：账号正确，密码错误。
    # 预取结果
    expected = {"code": 1, "msg": "账号或密码不正确"}
    result = login_check("python24", "lemon")
    print(result)
    if expected == result:
        print("用例执行通过")
    else:
        print("用例执行未通过")