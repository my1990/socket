'''
简单的ftp服务器，只有get(下载) put(上传) dir(查看目录) help（查看帮助） 功能
'''

import socket,os

server = socket.socket()
host = "127.0.0.1"
server.bind((host,888))
server.listen(5)
print("服务器已启动~\n")

while True:
    conn, addr = server.accept()
    print("new listen:", addr)
    while True:
        print("等待新的指令---")
        cmd_data = conn.recv(1024).decode()    #接收数据
        if not cmd_data:
            print("客户端已断开\n")
            break

        cmd = cmd_data.split()[0]        #接收用户的命令
        #print("接收命令~：", cmd)

        if cmd == "get":
            filename = cmd_data.split()[1]
            if os.path.isfile(filename):               #判断文件是否存在
                file_size = os.stat(filename).st_size  #判断文件大小
                conn.send(str(file_size).encode())     #发送文件大小
                conn.recv(1024)  #再收一次包，免得发生沾包问题
                print("file_szie_get:",file_size)
                f = open(filename,"rb")
                data = f.read()
                f.close()
                conn.send(data)  #发送文件
            else:
                conn.send("文件不存在".encode())
                print("文件不存在\n")
        elif cmd == "put":
            file_size_put = conn.recv(1024).decode()  #接收文件大小
            print("file_size_put:", file_size_put)
            conn.send(b"ack")              #返回ack,避免沾包
            resv_size_put = 0  # 初始文件大小
            f = open(cmd_data.split()[1] + ".put", "wb")
            while resv_size_put != int(file_size_put):
                data = conn.recv(1024)
                resv_size_put += len(data)
                f.write(data)
                #print("已接收：", resv_size_put, "总大小：", file_size_put)
            else:
                print("接收完毕,共接收%s字节" % file_size_put)
                f.close()

        elif cmd == "dir":
            cmd_resv = os.popen(cmd).read()
            conn.send(str(len(cmd_resv.encode("utf-8"))).encode("utf-8")) #把结果传过去
            print(len(cmd_resv.encode()))
            conn.send(cmd_resv.encode("utf-8"))                            #发送结果

        else:
            pass





