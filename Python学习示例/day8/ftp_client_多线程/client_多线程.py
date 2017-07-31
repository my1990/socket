
import os
import zhuce,login

def client_ftp():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录
    print("┌┬┬┬┬┬┬┬┬┬┬┬┬┐")
    print("├     TFP  Client        ┤")
    print("├     1、登录账号        ┤")
    print("├     2、注册账号        ┤")
    print("├     3、显示账号        ┤")
    print("└┴┴┴┴┴┴┴┴┴┴┴┴┘")

    while True:
        num = input(">>:")
        if num == '1':
            login.login()
        elif num == '2':
            zhuce.zhuce()
        elif num == '3':
            USER_DIR = BASE_DIR + '\\ftp_server_多线程\\conf\\users\\'
            dirs = os.listdir(USER_DIR)
            if len(dirs) == 0:
                print("当前无用户")
                continue
            else:
                print("当前账户如下：")
                for file in dirs:
                    print("用户名:",file)
                    continue
        elif num == 'q' or num == 'Q':
            print("bye-bye")
            exit(0)
        else:
            print("无效输入")
            continue

if __name__ == "__main__":
    client_ftp()
