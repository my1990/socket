'''
功能：查看用户的评论
输入用户UID后，搜索acfun网站文章区该用户的所有的评论。
'''
import requests
import re

def get_item():  #获取所有文章的ac号
    try:
        list = []  #存文章区文章编号
        tag_list = [ '164','73','74','110' ] #164是游戏区，73是工作情感区，74是动漫区，110是综合区
        for tag in tag_list:
            listID = 1  #每一个区的列表
            url_list = 'http://www.acfun.cn/v/list'+ tag + '/index_'+str(listID)+'.htm'
            list_source = request_session.get(url_list).text

            total_page_re = re.compile(r'<span class="hint">当前位置：(\d)*/(\d*)页</span>')
            total_page = total_page_re.findall(list_source)[0][1]   #文章总列表数

            while int(listID) <= int(total_page):
                item_re = re.compile(r'</span><a href="/a/ac(\d*)" target="_blank" title="(.*?)" class="title">(.*?)</a>')
                item = item_re.findall(list_source)

                for i in item:
                    list.append(i[0])
                listID += 1
        return list

    except BaseException as b:
        print("ERROR:",b)


def get_user(user,passwd,user_uid):   #开始获取用户评论
    try:
        #每次运行前，先清空文件
        f = open('acfun评论.txt', 'w')
        f.close()

        print("目前ACFUN文章区共有%s篇文章。" % len(get_item()))

        currentPage = 1  # 第一页评论
        flag = 1
        for contentId in get_item():
            user_url = 'http://www.acfun.cn/comment_list_json.aspx?contentId='+str(contentId)+'&currentPage='+str(currentPage)
            url_source = request_session.get(user_url).json()   #评论区源码
            commentList = url_source['data']['commentList']  #评论人数，如果评论人数为空，说明页面错误或没人评论，跳过
            user_cid = url_source['data']['commentList']     #评论人编号，每个编号代码一个评论人信息，信息包括评论人用户名、头像、评论内容等

            totalPage = url_source['data']['totalPage']      #评论总页数
            if len(commentList) != 0:
                if currentPage <= totalPage:
                    for user1 in user_cid:                   #循环每一个用户
                        user = int(user1)
                        user_ID = int(url_source['data']['commentContentArr']['c'+str(user)]['userID'])             #用户UID
                        user_name = url_source['data']['commentContentArr']['c'+str(user)]['userName']         #用户名
                        if user_ID == user_uid:   #判断用户名与索要查找的用户名是否一致
                            user_content = url_source['data']['commentContentArr']['c'+str(user)]['content']   #评论的内容
                            user_postDate = url_source['data']['commentContentArr']['c'+str(user)]['postDate'] #评论时间

                            #将用户信息和评论写入文件
                            f1 = open('acfun评论.txt','a')
                            f1.write('userID:  '+ str(user_uid) + '\n')
                            f1.write('用户名:  '+ user_name + '\n')
                            f1.write('评论内容: '+ user_content + '\n')
                            f1.write('评论时间: '+ user_postDate + '\n\n\n')
                            f1.close()

                    currentPage += 1  #评论换页

            flag += 1
            print("目前正在获取第%s篇文章评论..." % flag)
    except BaseException as a:
        print("ERROR:",a)


if __name__ == "__main__":
    user = input("请输入你的acfun账号:")
    passwd = input("请输入你的acfun密码:")
    user_uid = input("请输入需要查找的用户UID:")

    if user_uid.isdigit():
        #登录
        request_session = requests.Session()  # 会话对象requests.Session能够跨请求地保持某些参数，比如cookies，即在同一个Session实例发出的所有请求都保持同一个cookies,而requests模块每次会自动处理cookies，这样就很方便地处理登录时的cookies问题
        data = {'username': user, 'password': passwd}
        url = 'http://www.acfun.cn/login.aspx'
        t = request_session.post(url, data=data)

        if  t.json()['success'] == True:
            #开始获取评论
            get_user(user,passwd,user_uid)
        else:
            print("\nERROR:密码或用户名输入错误\n")
    else:
        print("\nERROR:需要查找的用户UID必须为纯数字\n")









