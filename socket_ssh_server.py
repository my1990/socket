import socket,os

server = socket.socket()
host = "127.0.0.1"
server.bind((host,8888))
server.listen(5)
print("服务器已启动~\n")

while True:
    conn, addr = server.accept()
    print("new listen:", addr)
    while True:
        print("等待新的指令---")
        data = conn.recv(1024)    #接收数据
        if not data:
            print("客户端已断开\n")
            break
        print("接收数据：",data)
        cmd_res = os.popen(data.decode()).read()

        if len(cmd_res) == 0:
            cmd_res = "命令无效"
            print("命令无效")

        conn.send( str(len(cmd_res.encode("utf-8"))).encode("utf-8"))
        print(len(cmd_res.encode()))
        conn.send(cmd_res.encode("utf-8"))

