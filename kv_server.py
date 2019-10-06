import socket
import argparse
import threading
import requests
import os
parser=argparse.ArgumentParser()
parser.add_argument('--host',default='127.0.0.1')
parser.add_argument('--port',type=int,default=5678)
args=parser.parse_args()
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((args.host,args.port))
server_socket.listen(5)
dic={}#储存key-value对
key_list=[]#储存各种key
#new_socket_list=[]
def catch(url):#用来把数据写入文件
    r=requests.get(url)
    with open('result','wb') as f:
        f.write(r.content)
    
with open('auth.conf')as m:#储存密码
        u=m.read()
        u=u.rstrip()
        list1=u.split('\n')#list1=['test 1234','admin 12345']
        for i in range(2):
            w=list1[i].split()
            dic[w[0]]=w[1]#已经储存在字典里了
            key_list.append(w[0])

def server(new_socket):
    msg1=' '#定义一个全局变量，用来检测是否通过AUTH命令
    while True:
        data = new_socket.recv(1024)
        data=data.decode('utf-8')
        if 'URL' in data:
            if msg1=='0':
                ch2=data[4:]#字符串的分割
                num2=ch2.index(' ')
                key2=ch2[0:num2]
                z2=ch2[num2+1:]
                catch(z2)#创建文件，储存网页数据
                value2=os.path.getsize('result')
                if key2 in key_list:
                    msg=dic[key2]
                else:
                    key_list.append(key2)
                    dic[key2]=str(value2)
                    msg=str(value2)
            if msg1!='0':
                msg=' '   
        if 'AUTH' in data:
            ch1=data[5:] #字符串分割
            num1=ch1.index(' ')
            key1=ch1[0:num1]
            value1=ch1[num1+1:]
            if dic[key1]==value1:
                msg='0'
                msg1='0'
            else:
                msg='-1'
                msg1='-1'
        if 'SET' in data:
            try:
                char1=data[4:]##字符串分割
                num=char1.index(' ')
                key=char1[0:num]
                value=char1[num+1:]
                dic[key]=value
                key_list.append(key)
                continue
            except ValueError:
                msg='请输入正确指令！'
        if 'GET' in data:
            try:
                char2=data[4:]#GET 1的1
                if char2 in key_list:
                    msg=dic[char2]
                if char2 not in key_list:
                    msg=' '
                if ' ' in char2:
                    msg='请输入正确指令!'
            except ValueError:
                msg='请输入正确指令!'
        if 'AUTH' not in data and  'SET' not in data and  'GET' not in data and 'URL' not in data:
            msg='请输入正确指令!'
        new_socket.send(bytes(msg,encoding='utf-8'))
        
while True:
        new_socket,address=server_socket.accept()
        t=threading.Thread(target=server,args=(new_socket,))
        t.start() 
t.close()
   







    
