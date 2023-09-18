import re
import platform

dir_L_yml = "/home/frank/.config/clash/changfen.yml"
dir_W_yml = "D:\\project\\python\\learning\\spider\\changfen_vpn\\2888.yml"
dir_target_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1690535581328.yml"
dir_target_L_yml = "/home/frank/.config/clash/profiles/1665195083683.yml"

def get_os_type():
    return platform.system()

def filter_yml(os_type,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml):
    lineList = []
    matchPattern_hk = re.compile(r'香港|台湾|HK|中国|CN')
    matchPattern_dns = re.compile(r'119.29.29.29')
    if os_type == "Windows":
        dir_source_yml = dir_W_yml
        dir_target_yml = dir_target_W_yml
    if os_type == "Linux":
        dir_source_yml = dir_L_yml
        dir_target_yml = dir_target_L_yml
    file = open(dir_source_yml,"r",encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        elif matchPattern_hk.search(line):
            pass
        elif matchPattern_dns.search(line):
            lineList.append(line.replace("119.29.29.29","114.114.114.114"))
        else:
            lineList.append(line)
    file.close()
    file = open(dir_target_yml,'w',encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()

def main(dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml):
    osType = get_os_type()
    print(osType)
    filter_yml(osType,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml)

if __name__ == "__main__":
    main(dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml)    