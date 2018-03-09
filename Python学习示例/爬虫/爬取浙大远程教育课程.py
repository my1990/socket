"""
浙大远程教育网站登录后可以看到自己的课程，但修改URL 课程kcdmb_id后，也可以看到其他人课程
url = http://ycjy.scezju.com/xxpt/kc/kcIndexGetCd.action?kcdmb_id=34&user_id=232167&role_id=5
本次就爬取所以课程，并保存下来,同时写入数据库
"""
import re
import requests
from urllib import request
import pymysql
import time

url = 'http://ycjy.scezju.com/xxpt/yhLogin.action' #登录url

def get_yzm():
    request.urlretrieve('http://ycjy.scezju.com/xxpt/yzm.jsp','./yzm.jpeg')
    yzm = input("验证码：")
    return yzm

def login(username,password):
    try:
        f1 = open('浙大远程教育课程.txt','w')  #每次运行先清空文件
        f1.close()

        post_data = {'yhm': username,
                     'mm': password,
                     'yzm': get_yzm()
                     }
        login_session = requests.Session()
        login = login_session.post(url, data=post_data).text

        sid_re = re.compile(r'<input type="hidden" name="sid" id="sid" value="(\w*.server1)"/>')
        sid = sid_re.findall(login)

        kcdmb_data = {'zybz': '2',
                      'sfzxkc': '0',
                      'sid': sid}

        db = pymysql.connect('192.168.254.2', 'root', '123', 'zheda' ,charset="utf8")  # 连接数据库
        cursor = db.cursor()

        id = 1  # 每个ID代表一个课程
        flag = 1
        while id <1350 :
            kcdmb_url = 'http://ycjy.scezju.com/xxpt/kc/kcIndexGetCd.action?kcdmb_id=' + str(id) + '&user_id=232167&role_id=5'  # 课程URL
            kcdmb_source = login_session.post(kcdmb_url,kcdmb_data).text

            kc_re = re.compile(r'<title>(.*?)_课程首页</title>')
            kc = kc_re.findall(kcdmb_source)

            if len(kc) != 0:
                kc_string = '\n课程名称:' + str(kc[0]) +  '\t\t\t课程id:' + str(id)
                print(kc_string)
                f = open('浙大远程教育课程.txt','a')
                f.write(kc_string)
                f.close()

                sql = " INSERT INTO kc (kc,kc_id) VALUES ( '%s',%s );" % ( kc[0],id )
                try:
                    cursor.execute(sql)  # 执行SQL
                    db.commit()  # 提交到数据库执行
                except BaseException as a:
                    print(a)
                    db.rollback()  # 出错时回滚
                    exit(0)


                flag += 1

            id += 1
        db.close()
        print( "共获取%s门课程" % flag )

    except BaseException as b:
        print("ERROR:",b)


start_time = time.time()
username = input("username:")
password = input("password:")
login(username,password)
stop_time = time.time()
print("\n程序运行时间:%.2f秒" % (stop_time - start_time))






