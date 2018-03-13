import socketserver,sys,os
import encryption_rsa
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录

class MyFtpServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        username = conn.recv(1024).decode()
        print("客户端已连接,连接地址：%s ,连接账号：%s" % (self.client_address[0],username))
        HOME_DIR = BASE_DIR + '\\data\\' + username
        os.chdir(HOME_DIR)  #切换到用户家目录

        while True:
            try:
                self.data = conn.recv(1024).decode()
                cmd = self.data.split()[0]  #获取操作命令
                print(cmd)

                if cmd == 'dir':
                    data = os.popen(cmd).read()
                    conn.send(str(len(data.encode())).encode())
                    conn.send(data.encode())
                elif cmd == 'get':
                    file_name = self.data.split()[1]
                    if os.path.exists(file_name):
                        file_size = os.stat(file_name).st_size
                        conn.send(str(file_size).encode())
                        conn.recv(1024)   #再收一次包，免得发生沾包问题
                        f = open(file_name,'rb')
                        data = f.read()
                        f.close()
                        conn.send(data)
                    else:
                        print("文件不存在~")
                        conn.send("文件不存在~".encode())
                elif cmd == 'put':
                    file_name = self.data.split()[1] + '.put'
                    file_size = conn.recv(1024).decode() # 文件大小
                    conn.send(b'ack')
                    resv_size = 0  # 初始文件大小
                    f = open(file_name, "wb")
                    while resv_size != int(file_size):
                        data = conn.recv(1024)
                        resv_size += len(data)
                        f.write(data)
                    else:
                        print("接收完毕,共接收%s字节" % file_size)
                        f.close()
                elif cmd == 'mkdir':
                    new_dir = self.data.split()[1]
                    if os.path.exists(new_dir):
                        messge = "目录已存在，无法新建~"
                        print(messge)
                        conn.send(messge.encode())
                    else:
                        os.mkdir(new_dir)  # 新建目录
                        conn.send("新建成功".encode())
                elif cmd == 'cd':
                    new_dir = self.data.split()[1]
                    if os.path.exists(new_dir):
                        os.chdir(new_dir)
                        conn.send(b' ')
                    else:
                        print("目录不存在，无法切换")
                        conn.send("目录不存在".encode())
                elif cmd == 'pwd':
                    conn.send(os.getcwd().encode())
                    print(os.getcwd())


            except ConnectionResetError:
                print("%s 客户端已断开" % self.client_address[0])
                break



if __name__ == '__main__':
    encryption_rsa.rsa_jia()
    host = '0.0.0.0'
    port = 8888
    server = socketserver.ThreadingTCPServer((host,port),MyFtpServer)
    print("FTP服务器已启动~")
    server.serve_forever()
