
import os,rsa,base64,json,binascii
import socket_conn_v2
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录
conf_path = BASE_DIR + '\\ftp_server_多线程\\conf\\'

def login():
    flag = 0
    while flag < 3:
        username = input("登录用户名:")
        password = input("登录密码:")
        if len(username) == 0 or len(password) == 0:
            print("账户或密码不能为空,请重新登录")
            flag += 1
            continue
        else:
            username_file = conf_path + 'users\\' + username
            with open(conf_path + 'private.pem', 'r') as f:       #导入私钥
                privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

            if os.path.exists(username_file):
                f = open(username_file,'r')
                cp = json.loads(f.read())
                f.close()
                cp_base64 = base64.b64decode(cp).decode()        #base64解密
                rsa_str = cp_base64[0:-len(username)]            #去掉解密后的账号符串
                rsa_sp = binascii.a2b_hex(rsa_str)               #转换成acsii编码
                rsa_pw = rsa.decrypt(rsa_sp, privkey).decode()   #rsa解密，最终密码
                if rsa_pw == password:
                    print("登录成功")
                    socket_conn_v2.client.conn(username)
                else:
                    print("密码错误，请重新登录")
                    flag += 1
                    continue
            else:
                print("用户名不存在")
                flag += 1
                continue
    else:
        print("登录错误次数超过三次，程序已退出")
        exit(0)
