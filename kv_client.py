# !-*- coding: utf-8 -*-
import socket
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--host',default='127.0.0.1')
parser.add_argument('--port',type=int,default=5678)
args=parser.parse_args()
try:
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((args.host,args.port))
except:
    print('连接地址有误，现已帮你切换到默认连接地址')
    print('若有需要，可以断开连接后重新输入地址')
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',5678))
while True:
     
    msg=input('请输入命令：')
    if 'QUIT' in msg:
        break
    if 'SET' in msg:
        client_socket.send(bytes(msg,encoding='utf-8'))
    else:
        client_socket.send(bytes(msg,encoding='utf-8'))
        data=client_socket.recv(1024)
        data=data.decode('utf-8')
        print(data)
   
client_socket.close()
            

