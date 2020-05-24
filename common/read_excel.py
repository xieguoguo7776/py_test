import openpyxl


# 用来保存用来数据
class CassData:
    """用来存储数据的临时类"""
    pass


class ReadExcel:

    def __init__(self, file_name, sheet_name):
        """
        初始化方法
        :param file_name:文件名
        :param sheet_name: 表单名
        """
        self.file_name = file_name
        self.sheet_name = sheet_name

    def open(self):
        """打开工作簿，选中表单"""
        self.wk = openpyxl.load_workbook(self.file_name)
        self.sh = self.wk[self.sheet_name]

    def close(self):
        """关闭工作簿，释放内存"""
        self.wk.close()

    def save(self):
        """保存工作簿，关闭工作簿"""
        self.wk.save(self.file_name)
        self.wk.close()

    def read_data(self):
        """

        :return: 返回列表嵌套字典数据
        """
        self.open()
        # 按行获取所有的格子
        rows = list(self.sh.rows)
        # 获取表头数据
        title = []
        for i in rows[0]:
            title.append(i.value)

        # 获取除表头的数据
        cases = []
        for row in rows[1:]:
            # 创建一个空列表，用来存储该行的数据
            data = []
            # 再次遍历该行每一个格子
            for i in row:
                # 将格子中的数据，添加到data中
                data.append(i.value)
            case = dict(zip(title, data))
            cases.append(case)
        # 关闭工作簿
        self.close()
        return cases

    def write_data(self, row, column, value):
        # 打开工作簿
        self.open()
        # 写入数据
        self.sh.cell(row=row, column=column, value=value)
        # 保存文件
        self.wk.save(self.file_name)
        # 关闭工作簿
        self.close()

    def read_data_obj(self):
        """

        :return: 返回列表嵌套对象数据
        """
        self.open()
        # 按行获取所有的格子
        rows = list(self.sh.rows)
        # 获取表头数据
        title = []
        for i in rows[0]:
            title.append(i.value)

        # 获取除表头的数据
        cases = []
        for row in rows[1:]:
            # 创建一个空列表，用来存储该行的数据
            data = []
            # 再次遍历该行每一个格子
            for i in row:
                # 将格子中的数据，添加到data中
                data.append(i.value)
                # 将表头和其他行数据打包，转化成列表
            case = list(zip(title, data))
            # 创建一个对象用来保存该行用例数据
            case_obj = CassData()
            # 遍历列表中该行用例数据，使用setattr设置为对象的属性和属性值
            for k, v in case:  # 对元组拆包
                setattr(case_obj, k, v)
            # 将随想添加到cases这个列表中
            cases.append(case_obj)
        # 关闭工作簿
        self.close()
        # 返回cases(包含所有用例数据对象的列表)
        return cases


if __name__ == '__main__':
    read_excel = ReadExcel("cases.xlsx", "login")
    data = read_excel.read_data_obj()
    print(data)
