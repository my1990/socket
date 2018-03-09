#
# 验证码原理：
# 后端随机生成字符串并写入 session
# 然后将字符串用gd库或imagick生成图片，在前端显示。
# 用户根据前端看到的验证码图片，输入验证码
# 后端根据用户输入的验证码与session中的验证码（后端之前生成的字符串）比较，一样则通过，不一样不通过
import re
import requests
from urllib import request
from bs4 import BeautifulSoup
url = 'http://ycjy.scezju.com/xxpt/yhLogin.action'

def get_yzm():
    r = request.urlretrieve('http://ycjy.scezju.com/xxpt/yzm.jsp','./yzm.jpeg')
    yzm = input("验证码：")
    return yzm


def login(username,password):
    post_data = {'yhm':username,
                 'mm':password,
                 'yzm':get_yzm()
                 }
    login_session = requests.Session()
    login = login_session.post(url,data=post_data).text

   #获取课程url源码
    subject_source = login_session.get(url='http://ycjy.scezju.com/xxpt/indexInit.action?sid=CjFspB-QWRArTfuh6UFFT0iZrXtEPHXpCZ0A&role_id=5&user_id=232167').text
    soup = BeautifulSoup(subject_source,'html.parser')  #创建 beautifulsoup 对象
    source_list = soup.find_all('tbody') #查找所以tbody标签

    #获取正在学习的课程
    zxlist_source = source_list[0] #正在学习的课程的源码
    zxlist =zxlist_source.find_all('h1')  #获取课程标签
    print("-----正在学习课程如下：-------")
    for zx in range(len(zxlist)):
        print(zxlist[zx].string) #打印课程

    #获取已经学过的课程
    yxlist_source = source_list[1] #已经学过的课程的源码
    yxlist =yxlist_source.find_all('h1')  #获取课程标签
    print("\n-----已经学习课程如下：-------")
    for yx in range(len(yxlist)):
        print(yxlist[yx].string) #打印课程

    # 获取还未学习的课程
    wxlist_source = source_list[2]  # 还没学习的课程的源码
    wxlist = wxlist_source.find_all('h1')  # 获取课程标签
    print("\n----还未学习课程如下：-------")
    for wx in range(len(wxlist)):
        print(wxlist[wx].string)  # 打印课程


if  __name__ == '__main__':
    username = input("username:")
    password = input("password:")
    login(username,password)













