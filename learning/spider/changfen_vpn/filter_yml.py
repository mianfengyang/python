import re

def filter_yml():
    lineList = []
    matchPattern_hk = re.compile(r'香港|台湾')
    matchPattern_dns = re.compile(r'119.29.29.29')
    file = open("changfen.yml","r",encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            print("Read file End or Error")
            break
        elif matchPattern_hk.search(line):
            pass
        elif matchPattern_dns.search(line):
            lineList.append(line.replace("- 119.29.29.29","- 114.114.114.114"))
        else:
            lineList.append(line)
    file.close()
    file = open(r'target.yml', 'w',encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()

if __name__ == "__main__":
    filter_yml()