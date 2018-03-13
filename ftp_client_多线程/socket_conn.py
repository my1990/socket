
import socket,os,hashlib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录

def conn(usrname):
    print("    welcome to FTP Server     ")
    print("当前目录：", os.getcwd())
    client = socket.socket()
    client.connect(('127.0.0.1',8888))
    client.send(usrname.encode())
    while True:
        cmd = input(">>:").strip()
        if len(cmd) == 0:
            print("请输入命令:")
            continue
        #print("操作命令：",filename.split()[0])

        if cmd.split()[0] == "get" and len(cmd.split()) == 2:    #判断输入的命令是否 get开头
            client.send(cmd.encode("utf-8"))              #把命令发给server
            file_size = client.recv(1024).decode()              #获取所要接收数据的大小
            #print("文件总大小：",file_size)
            if file_size.isdigit():                             #判断接收到的数据是否为数字，不为数字说明文件不存在
                client.send("接收到文件大小，可以开始传送数据".encode())
                resv_size = 0        # 初始文件大小
                f = open(cmd.split()[1] + ".get", "wb")
                while resv_size != int(file_size):
                    data = client.recv(1024)
                    resv_size += len(data)
                    f.write(data)
                    #print("已接收：", resv_size,"总大小：",file_size)
                else:
                    print("接收完毕,共接收%s字节" % file_size)
                    print(os.getcwd())
                    f.close()
            else:
                print("%s文件不存在" % cmd.split()[1])

        elif cmd.split()[0] == "put" and len(cmd.split()) == 2:
            if len(cmd.split()) == 2:
                put_filename = cmd.split()[1]
                if os.path.isfile(put_filename):
                    client.send(cmd.encode("utf-8"))  # 把命令发给server
                    file_size = os.stat(put_filename).st_size  # 判断文件大小
                    print("文件大小：",file_size)
                    client.send(str(file_size).encode())  # 发送文件大小
                    client.recv(1024)  # 再收一次包，免得发生沾包问题
                    #print("已接收ack")
                    f = open(put_filename, "rb")
                    data = f.read()
                    f.close()
                    client.send(data)  # 发送文件
                    print("文件已上传成功")
                else:
                    print("文件不存在，无法上传")
            else:
                print("上传时，必须写明文件名,且同时只能上传一个文件")
        elif cmd.split()[0] == "mkdir" and len(cmd.split()) == 2:
            client.send(cmd.encode())
            print(client.recv(1024).decode())
        elif cmd.split()[0] == "cd" and len(cmd.split()) == 2:
            if  len(cmd.split()) == 2:
                client.send(cmd.encode())
                print(client.recv(1024).decode())
            else:
                print("cd命令语法出错")
        elif cmd.split()[0] == 'pwd' and len(cmd.split()) == 1:
            client.send('pwd'.encode())
            print(client.recv(1024).decode())

        elif cmd.split()[0] == "dir" and len(cmd.split()) == 1 :
            client.send(cmd.split()[0].encode())
            cmd_resv_size = client.recv(1024)          #接收命令结果大小
            print("命令结果大小：",cmd_resv_size)
            size = 0
            while size != int(cmd_resv_size):
                cmd_resv = client.recv(1024)
                size += len(cmd_resv)
                print(cmd_resv.decode())


        elif  cmd.split()[0] == "help" or  cmd.split()[0] == "h":
            print("\t          -------- 命令菜单 ----------- \n \
                 -------- get: 下载文件 ------ \n \
                 -------- put: 上传文件 ------ \n \
                 -------- dir: 查看目录 ------ \n \
                 -------- help: 查看帮助 ----- \n \
                "
                  )
        else:
            print("命令 %s 不存在" % cmd)

    client.close()




