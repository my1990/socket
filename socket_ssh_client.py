#因为一个中文长度没编码前是1 编码后是3，所以如果俩边判断长度不统一(一边编码前判断长度，一边编码后判断)，会导致实际接收数据大小不一致
# len("一")   ！=  len("一".encode())
#socket只能传输二进制，所以传输的数据要先encode()
import socket,math

client = socket.socket()
client.connect(('127.0.0.1',8888))

while True:
    cmd = input(">>:\n").strip()
    if len(cmd) == 0:
        print("请输入命令：\n")
        continue
    client.send(cmd.encode("utf-8"))
    cmd_resv_size = int(client.recv(1024))      #获取所要接收数据的大小

    resv_size = 0
    while resv_size != cmd_resv_size:
        cmd_resv =client.recv(1024)
        resv_size += len(cmd_resv)
        print(cmd_resv.decode())

    else:
        print("接收完毕,共接收%s字节" % resv_size)

client.close()