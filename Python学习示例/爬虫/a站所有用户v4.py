import re,pymysql
import threading,queue
import requests
import logging,time
#获取所有文件标识符
def href():
    type_list = ['164', '73', '74','75','110']  # 164是游戏区，73是工作情感区，74是动漫区，75是轻小说区，110是综合区
    for tag in type_list:
        list_id = 1
        url = 'http://www.acfun.cn/v/list' + tag + '/index_' + str(list_id) + '.htm'
        try:
            page_source = request_session.get(url).text
            total_page_re = re.compile(r'当前位置：(\d)*/(\d*)页')
            total_page = total_page_re.findall(page_source)[0][1]  # 文章总列表数
            d = 2 # 每个文章类型显示有20000页，实际上并没有这么多，后面很多页内容其实是空的，设置d参数就是过滤掉这些空内容的
            while int(list_id) <= int(total_page) and int(d) != 1:

                item_re = re.compile(r'</span><a href="/a/ac(\d*)" target="_blank" title="(.*?)" class="title">(.*?)</a>')
                item = item_re.findall(page_source)
                url = 'http://www.acfun.cn/v/list' + tag + '/index_' + str(list_id) + '.htm'
                page_source = request_session.get(url).text
                d_re = re.compile(r'<span class="hint">当前位置：(\d*)/(\d*)页</span>')  # 判断文件列表是否为空
                d = int(d_re.findall(page_source)[0][1])
                for i in item:
                    href_id = i[0]
                    data = [tag,href_id]
                    q.put(data)
                    print("文章号:%s放入队列,文章列表:%s,文章类型:%s" % (href_id,list_id,tag))
                list_id += 1
        except BaseException as e:
            print("ERROR_href:",e)
            logging.error("href_id",href_id,e)
            continue



def get_user(name):
    host = 'rm-uf643ap9b01399w94o.mysql.rds.aliyuncs.com'
    conn = pymysql.connect(host=host, port=3306, user='root', passwd='Qw1234567', db='acfun_bak',charset="utf8")
    cursor = conn.cursor()
    sql = "TRUNCATE TABLE `acfun_users`;DELETE  FROM  `acfun_users`;"
    cursor.execute(sql)  # 执行SQL
    conn.commit()  # 提交到数据库执行
    flag = 1
    while True:
        if not q.empty():
            flag = 1 #队列不为空，重置时间
            data = q.get()
            a = data[1]  #文章号
            tag = data[0] #文章类型
            print("从队列中取得文章号：%s  文章类型：%s" % ( a, tag))
            #a = 3916933
            id = 1
            url = 'http://www.acfun.cn/comment_list_json.aspx?contentId=' + str(a) + '&currentPage=' + str(id)
            try:
                data = request_session.get(url).json()
                total_page = data['data']['totalPage']  #总评论页
                user_cid = data['data']['commentList']  # 评论人数，如果评论人数为空，说明页面错误或没人评论，跳过
                if user_cid:
                    while id <= int(total_page):
                        url = 'http://www.acfun.cn/comment_list_json.aspx?contentId=' + str(a) + '&currentPage=' + str(id)
                        data = request_session.get(url).json()
                        user_dict = data['data']["commentContentArr"]  # 所有用户信息，包括用户名、uid、评论等
                        for user in user_dict:
                            user_name = user_dict[user]['userName']  #用户名
                            user_id = user_dict[user]["userID"]       #用户id
                            user_id = int(user_id)
                            if user_id != '-1' and user_id not in acfun_list: #user_id= -1.0表示该用户被删除评论，也就获取不到用户名和uid
                                acfun_list.append(user_id)
                                cursor = conn.cursor()
                                sql = "INSERT INTO acfun_users (page_type,page_id,uuid,user_name) VALUES ('%s','%s','%s','%s');" % (int(tag),int(a),user_id, user_name)
                                try:
                                    cursor.execute(sql)  # 执行SQL
                                    conn.commit()  # 提交到数据库执行
                                except BaseException:
                                    print("ERROR")
                                    conn.rollback()  # 出错时回滚
                                logging.info(u"Thared-%s 用户名:%s  UUID:%s" % (name, user_name, user_id))
                                print("Thared-%s 用户名:%s  UUID:%s" % (name, user_name, user_id))
                                print("------------当前acfun_list长度为：%s-----------------" % len(acfun_list))
                            # else:
                            #     if user_id not in acfun_list1:
                            #         acfun_list1.append(user_id)
                            #         print("uuid为%s之前已收录,或该用户已被删除评论~" % user_id)
                            #         logging.warning(u"用户名:%s  UUID:%s 之前已收录,或该用户已被删除评论" % (user_name, user_id))

                        id += 1
                    print("文章%s内所有评论人信息已获取完毕~" % a)
                else:
                    print("文章号%s无人评论~" % a)
            except BaseException as e:
                print("ERROR_get_users:", e)
                logging.error("get_users 文章类型:%s 文章号:%s  %s" % (tag,a,e))
                continue
            except IndexError:
                print("ERROR_get_users:", e)
                logging.error("列表已满" ,e)
                return  "列表已满"
        else:
            if flag < 300:  #队列空就等一秒，如果等待5分钟后，队列还是空，视为所有文章已抓取完毕，退出程序
                print("队列中无数据")
                print("队列空：---------当前acfun_list长度为：%s-----------" % len(acfun_list))
                time.sleep(1)
                flag += 1
                logging.info("队列空，等待%s秒钟" % flag)
            else:
                logging.info("All work is Done!")
                return "All work is Done!"
    conn.close()


if __name__ == "__main__":
    request_session = requests.Session()
    q = queue.Queue(maxsize=10)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='acfun.log',
                        filemode='w+')

    f = open('acfun.log','w')
    f.close()
    acfun_list = []  #存放之前没记录的用户
    acfun_list1 = [] #存放之前已记录的用户

    href1 = threading.Thread(target=href)
    href1.start()

    t_list = []
    for i in range(10):
        get_user1 = threading.Thread(target=get_user,args=(i,))
        get_user1.start()
        t_list.append(get_user1)
    for t in t_list:
        t.join()
