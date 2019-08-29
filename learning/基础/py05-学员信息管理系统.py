#coding=utf-8

"""
=============================================================
#   project: python
#      file: py05-学员信息管理系统.py
#    author: mianfeng.yang
#      date: 2019-08-29 15:41:19
=============================================================
"""
def menu():
    print('=' * 80)
    print("1. 添加学员")
    print("2. 删除学员")
    print("3. 修改学员")
    print("4. 查询学员")
    print("5. 显示所有学员")
    print("6. 退出系统")
    print('=' * 80)

# 存储学员信息
users = []
def add_user():
    """添加学员"""
    # 1. 用户输入：学号，姓名，手机号
    user_id = int(input("请输入学号："))
    user_name = input("请输入姓名：")
    user_pho = input("请输入手机号：")

    # 2. 判断学员是否已存在，不存在则添加，存在则提示
    global users
    user = {}

    # 2.1 判断学员 id 号 是否存在
    for i in users:
        if user_id == i['id']:
            print("学员已存在")
            return # 如果存在，提示，并退出函数体

    # 2.2 向字典中添加用户信息
    user['id'] = user_id
    user['name'] = user_name
    user['phone'] = user_pho
    users.append(user)

def del_user():
    """删除学员"""
    # 根据学员的姓名进行删除学员
    global users
    user_name = input("请输入学员的姓名：")

    # 遍历所有学员列表,先判断学员信息是否存在，存在则将找到的学员信息删除，不存在则给出提示
    for i in users:
        if user_name == i['name']:
            users.remove(i)
            print("学员 {} 存在并已删除".format(user_name))
            break
    else:
        print("学员 {} 不存在".format(user_name))

def mod_user():
    """修改学员"""
    pass

def ser_user():
    """查询学员"""
    # 根据学员姓名进行查询
    user_name = input("请输入要查询的学员的姓名：")
    print("=" * 80)
    for i in users:
        if user_name == i['name']:
            print("id:{}\t name:{}\t phone:{}".format(i['id'], i['name'], i['phone']))
            # print("name:{}".format(i['name']))
            # print("phone:{}".format(i['phone']))
            print("=" * 80)
            break
    else:
        print("学员 {} 不存在".format(user_name))

def dis_user():
    """显示所有学员"""
    print("=" * 80)
    for i in users:
        print("id:{}\t name:{}\t phone:{}".format(i['id'], i['name'], i['phone']))
        # print("id:{}".format(i['id']))
        # print("name:{}".format(i['name']))
        # print("phone:{}".format(i['phone']))
        print("=" * 80)
    print("所有学员信息显示完成，并回主菜单")

def main():
    """主函数"""
    # 循环显示菜单直到用户选择退出
    while True:
        menu()
        get_user_input = int(input("请输入菜单对应的数字："))
        if get_user_input == 1:
            add_user()
        elif get_user_input == 2:
            del_user()
        elif get_user_input == 3:
            mod_user()
        elif get_user_input == 4:
            ser_user()
        elif get_user_input == 5:
            dis_user()
        elif get_user_input == 6:
            return
        else:
            print("请输入正确的数字……")



if __name__ == '__main__':
    main()