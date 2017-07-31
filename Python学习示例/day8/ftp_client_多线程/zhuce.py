# 账户注册

import os,rsa,json,binascii,base64
import login

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录
conf_path = BASE_DIR + '\\ftp_server_多线程\\conf\\'

def zhuce():
    print("欢迎来到注册页面，请填写用户名及密码")
    flag = 1
    while flag <= 5:
        username = input("username:")
        password = input("password:")
        if len(username) == 0 or len(password) == 0:
            print("账户或密码不能为空")
            flag += 1
            continue
        else:
            if len(username) < 3 or len(password) < 3:
                print("密码或用户名不能小于3位\n")
                flag += 1
                continue
            else:
                username_file = conf_path + 'users\\'+ username
                if os.path.exists(username_file):
                    print("%s账户已存在，无法再次注册,回车继续注册，按q退出" % username)
                    choise = input(">>:")
                    if choise == 'q' or choise == 'Q':
                        print("已退出注册")
                        exit(0)
                    else:
                        flag += 1
                        continue

                else:
                    # 导入公钥文件
                    with open(conf_path + 'public.pem','r') as f:
                        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
                    # 公钥加密
                    crypto = rsa.encrypt(password.encode(), pubkey)  #rsa加密后的密码
                    crypto1 = binascii.b2a_hex(crypto).decode()      #加密后的密码转换为十六进制的字符串
                    #print("rsa:",crypto1)
                    base_pw_str = crypto1 + username        #将加密后的字符串加上用户名,然后在用base64加密
                    base_pw = base64.b64encode(base_pw_str.encode('utf-8')).decode()
                    #print("base:",base_pw)
                    f = open(username_file,'w')
                    f.write(json.dumps(base_pw))   #将加密后的密码写入文件
                    f.close()
                    os.mkdir(BASE_DIR + '\\ftp_server_多线程\\data\\' + username)  #新建用户家目录
                    print("已注册成功，请登录")
                    login.login()
    else:
        print("注册次数超过五次，程序退出")

