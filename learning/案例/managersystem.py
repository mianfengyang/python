#coding=utf-8

"""
=============================================================
#   project: python
#      file: managersystem.py
#    author: mianfeng.yang
#      date: 2019-09-09 11:08:01
=============================================================
"""
from student import *


class StudentManager(object):
    def __init__(self):
        # 存储所有的学员信息
        self.student_list = []

    # 一. 程序入口函数，启动程序后执行的函数
    def run(self):
        # 1. 加载学员信息
        self.load_student()
        while True:
            # 2. 显示功能菜单
            self.show_menu()
            # 3. 用户输入序号，选择功能菜单
            menu_num = int(input("请输入功能序号： "))
            # 4. 根据用户的输入进入相应功能
            if menu_num == 1:
                # 添加学员
                self.add_student()
            elif menu_num == 2:
                # 删除学员
                self.del_sutdent()
            elif menu_num == 3:
                # 修改学员
                self.modify_student()
            elif menu_num == 4:
                # 查询学员
                self.search_student()
            elif menu_num == 5:
                # 显示所有学员
                self.show_student()
            elif menu_num == 6:
                # 保存学员
                self.save_student()
            elif menu_num == 7:
                # 退出程序
                break

# 二. 系统功能函数
# 2.1 显示功能菜单
    @staticmethod
    def show_menu():
        print('=' * 20)
        print('请选择功能菜单： ')
        print('1： 添加学员： ')
        print('2： 删除学员： ')
        print('3： 修改学员： ')
        print('4： 查询学员： ')
        print('5： 显示所有： ')
        print('6： 保存学员： ')
        print('7： 退出系统： ')
        print('=' * 20)

# 2.2 添加学员
    def add_student(self):
        name = input("姓名： ")
        gender = input("性别： ")
        tel = input("手机号： ")

        student = Student(name, gender, tel)
        self.student_list.append(student)


# 2.3 删除学员
    def del_sutdent(self):
        del_name = input("请输入要删除的学员姓名：")

        for i in self.student_list:
            if i.name == del_name:
                self.student_list.remove(i)
                print(f'删除学员：{i.name} 成功：')
                break
        else:
            print('查无此人')


# 2.4 修改学员
    def modify_student(self):
        modify_name = input("请输入要修改的学员姓名：")
        modify_tel = int(input("请输入新的手机号："))

        for i in self.student_list:
            if i.name == modify_name:
                i.name = input('请输入新名字：')
                i.gender = input('请输入性别：')
                i.tel = modify_tel
                print(f'修改学员信息成功：姓名：{i.name} 性别：{i.gender} 手机号：{i.tel}')
                break
        else:
            print('查无此人')


# 2.5 查询学员
    def search_student(self):
        search_name = input("请输入要查询的学员姓名：")
        for i in self.student_list:
            if i.name == search_name:
                print(f"找到学员信息：姓名：{i.name} 性别：{i.gender} 手机号：{i.tel}")
                break
        else:
            print('查无此人')


# 2.6 显示所有
    def show_student(self):
        print("姓名\t性别\t手机号")
        print('=' * 20)
        for i in self.student_list:
            print(f'{i.name}\t{i.gender}\t{i.tel}')

        print('=' * 20)

# 2.7 保存
    def save_student(self):
        f = open('students.data', 'w')
        new_list = [i.__dict__ for i in self.student_list]
        f.write(str(new_list))
        f.close()

# 2.8 加载学员信息
    def load_student(self):
        try:
            f = open('students.data', 'r')
        except:
            f = open('students.data', 'w')
        else:
            data = f.read() # 字符串
            new_list = eval(data)
            self.student_list = [Student(i['name'], i['gender'], i['tel']) for i in new_list]
        finally:
            f.close()

if __name__ == '__main__':
    pass