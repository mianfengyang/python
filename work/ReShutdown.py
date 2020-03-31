# coding=utf-8

"""
==============================================================
# @Time    : 2020/3/30 14:36
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : ReShutdown
# @Software: PyCharm
==============================================================
"""

"""
shutdown命令的语法格式是：shutdown [-i/-l/-s/-r/-a][-f][-m[\ComputerName]][-t XX][-c"message"][-d[u][p]:xx:yy]

各参数的含义为

-i 显示图形界面对话框；

-l 注销当前用户(默认设置会注销当前用户)；

-s 关闭计算机；

-r 关闭之后立即重新启动；

-a 终止关闭，除了-l和ComputerName外，系统将忽略其他参数。在超时期间，你只能使用-a；

-f 强制运行要关闭的应用程序；

-m [\\ComputerName]指定要关闭的计算机，不指定默认为本机；

-t XX将用于系统关闭的定时器设置为XX秒，默认是20秒；

-c "message"指定将在“系统关闭”窗口中的“消息”区域显示消息，最多可以使用127个字符；

-d [u][p]:xx:yy列出系统关闭的原因代码，为系统关机日志记录使用；

Reasons on this computer:
(E = Expected U = Unexpected P = planned, C = customer defined)
Type    Major    Minor    Title
 
 U      0    0    Other (Unplanned)
E       0    0    Other (Unplanned)
E P     0    0    Other (Planned)
 U      0    5    Other Failure: System Unresponsive
E       1    1    Hardware: Maintenance (Unplanned)
E P     1    1    Hardware: Maintenance (Planned)
E       1    2    Hardware: Installation (Unplanned)
E P     1    2    Hardware: Installation (Planned)
E       2    2    Operating System: Recovery (Planned)
E P     2    2    Operating System: Recovery (Planned)
  P     2    3    Operating System: Upgrade (Planned)
E       2    4    Operating System: Reconfiguration (Unplanned)
E P     2    4    Operating System: Reconfiguration (Planned)
  P     2    16    Operating System: Service pack (Planned)
        2    17    Operating System: Hot fix (Unplanned)
  P     2    17    Operating System: Hot fix (Planned)
        2    18    Operating System: Security fix (Unplanned)
  P     2    18    Operating System: Security fix (Planned)
E       4    1    Application: Maintenance (Unplanned)
E P     4    1    Application: Maintenance (Planned)
E P     4    2    Application: Installation (Planned)
E       4    5    Application: Unresponsive
E       4    6    Application: Unstable
 U      5    15    System Failure: Stop error
 U      5    19    Security issue
E       5    19    Security issue
E P     5    19    Security issue
E       5    20    Loss of network connectivity (Unplanned)
 U      6    11    Power Failure: Cord Unplugged
 U      6    12    Power Failure: Environment
  P     7    0    Legacy API shutdown
"""
import os

import paramiko


win_hosts = ["192.168.21.10", "192.168.21.11", "192.168.22.10","192.168.22.11"]
linux_hosts = ["192.168.21.15", "192.168.22.15", "192.168.22.21"]
msg = "市电异常，将在60秒后关机"

test_win_host = "192.168.21.53"
test_lin_host = "192.168.21.30"
user = "root"
command = "shutdown -h +1"

def shutdown_win(list):
    for host in list:
        os.system("shutdown /s /m \\\\{h} /t {time} /d u:6:12 /c {message}".format(h=host, time=60, message=msg))

def ssh_exec_command(host, user, command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connect to:" + host)
        password = input(host + " password:")
        ssh_client.connect(host, 22, user, password)
        
        print("command: " + host + " " + command)
        std_in, std_out, std_err = ssh_client.exec_command(command, get_pty=True)
        #std_in.write(password + '\n')
        
        for line in std_out:
            print(line.strip("\n"))
        for line in std_err:
            print(line.strip("\n"))
        
        ssh_client.close()
    except Exception as e:
        print("error: " + str(e))

       
        
if __name__ == '__main__':
    # shutdown_win(win_hosts)
    # os.system("shutdown -s -m \\\\{h} -t {time} -d u:6:12 -c {message}".format(h=test_lin_host, time=60, message=msg))
    #ssh_exec_command(test_lin_host, user, command)