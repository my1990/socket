
import socket,os,hashlib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录

class conn_client():
    def __init__(self):
        self.client = socket.socket()

    def conn(self,username):
        print("    welcome to FTP Server     ")
        print("当前目录：", os.getcwd())
        self.client.connect(('127.0.0.1',8888))
        self.client.send(username.encode())
        while True:
            cmd = input(">>:").strip()
            if len(cmd) == 0:
                print("请输入命令:")
                continue
            #print("操作命令：", cmd.split()[0])

            if hasattr(self,cmd.split()[0]):
                func = getattr(self,cmd.split()[0])
                func(cmd)
            else:
                print("无此命令")
    def get(self,cmd):
        if len(cmd.split()) == 2:
            self.client.send(cmd.encode("utf-8"))  # 把命令发给server
            file_size = self.client.recv(1024).decode()  # 获取所要接收数据的大小
            # print("文件总大小：",file_size)
            if file_size.isdigit():  # 判断接收到的数据是否为数字，不为数字说明文件不存在
                self.client.send("接收到文件大小，可以开始传送数据".encode())
                resv_size = 0  # 初始文件大小
                f = open(cmd.split()[1] + ".get", "wb")
                while resv_size != int(file_size):
                    data = self.client.recv(1024)
                    resv_size += len(data)
                    f.write(data)
                    # print("已接收：", resv_size,"总大小：",file_size)
                else:
                    print("接收完毕,共接收%s字节" % file_size)
                    print(os.getcwd())
                    f.close()
            else:
                print("%s文件不存在" % cmd.split()[1])
        else:
            print("get 后面只能跟一个参数")

    def put(self,cmd):
        if len(cmd.split()) == 2:
            put_filename = cmd.split()[1]
            if os.path.isfile(put_filename):
                self.client.send(cmd.encode("utf-8"))  # 把命令发给server
                file_size = os.stat(put_filename).st_size  # 判断文件大小
                print("文件大小：", file_size)
                self.client.send(str(file_size).encode())  # 发送文件大小
                self.client.recv(1024)  # 再收一次包，免得发生沾包问题
                # print("已接收ack")
                f = open(put_filename, "rb")
                data = f.read()
                f.close()
                self.client.send(data)  # 发送文件
                print("文件已上传成功")
            else:
                print("文件不存在，无法上传")
        else:
            print("上传时，必须写明文件名,且同时只能上传一个文件")

    def mkdir(self,cmd):
        if len(cmd.split()) == 2:
            self.client.send(cmd.encode())
            print(self.client.recv(1024).decode())
        else:
            print("%s 语法错误" % cmd.split()[0])

    def cd(self,cmd):
        if len(cmd.split()) == 2:
            self.client.send(cmd.encode())
            print(self.client.recv(1024).decode())
        else:
            print("%s 语法错误" % cmd.split()[0])
    def pwd(self,cmd):
        if len(cmd.split()) == 1:
            self.client.send('pwd'.encode())
            print(self.client.recv(1024).decode())
        else:
            print("%s 语法错误" % cmd.split()[0])

    def dir(self,cmd):
        if len(cmd.split()) == 1:
            self.client.send(cmd.split()[0].encode())
            cmd_resv_size = self.client.recv(1024)  # 接收命令结果大小
            print("命令结果大小：", cmd_resv_size)
            size = 0
            while size != int(cmd_resv_size):
                cmd_resv = self.client.recv(1024)
                size += len(cmd_resv)
                print(cmd_resv.decode())
        else:
            print("%s 语法错误" % cmd.split()[0])
    def help(self,cmd):
        if len(cmd.split()) == 1:
            HELP_FILE = BASE_DIR + "\\ftp_server_多线程\\conf\\help.txt"
            f = open(HELP_FILE,'r')
            print(str(f.read()))
            f.close()

        else:
            print("%s 语法错误" % cmd.split()[0])




client = conn_client()
#client.conn('123')






