from bs4 import BeautifulSoup
import requests,queue
import math,re,os
import threading
import time,sys
sys.setrecursionlimit(10000)

def get_job_info(proxies,step,step1):
    if not q.empty():
        job_dict1 = q.get()
        id = job_dict1['job_url']
        url = Base_url + str(id) + '?ka=job-7'
        try:
            job_data_source = requests_session.get(url,headers=headers,proxies=proxies).text
        except BaseException as z:
            if str(z)[0:4] == 'HTTP':
                q.put(job_dict1)
                print("此代理IP无法使用，换个ip继续抓",proxies)
                step1 += 1

            else:
                print(z)
        else:
            try:
                    job_soup = BeautifulSoup(job_data_source,'lxml')
                    text_sour = job_soup.find_all(attrs=['job-sec'])[0].find(attrs=['text'])
                    text = str(text_sour).replace('<br/>','').replace('<div class="text">','').replace('</div>','').replace('\xa0','').strip()
                    tag_sour = job_soup.find_all(attrs=['job-tags'])
                    tag_re = re.compile(r'<span>(.*?)</span>')
                    tag = tag_re.findall(str(tag_sour))
                    job_dict1['tag'] = tag           #工作标签
                    job_dict1['text'] = text         #工作职责
                    del job_dict1['job_url']
                    print(job_dict1)
        # f = open('wwwwww', 'a')
        # f.write(json.dumps(url))
        # f.write('\n')
        # f.close()
            except BaseException as zzz:
                print(zzz)
    else:
        print("队列中无数据")
        exit(0)


def get_info(proxies,page_id1):

    Base_url = 'http://www.zhipin.com/'
    url = Base_url + 'gongsi/r110874.html?page=' + str(page_id1) + '&ka=page-' + str(page_id1)
    print("url:",url)
    try:
     data_source = requests_session.get(url, headers=headers,proxies=proxies).text
    except BaseException as z:
        if str(z)[0:4] == 'HTTP':
            q1.put(page_id1)
            print("此URL待会爬取:",url)
        else:
            print(z)
    else:
        try:
            next_page_re = re.compile(r'<a href="(.*?)" ka="page-next" class="(.*?)"></a>')
            next_page = next_page_re.findall(data_source)[0]
            #print(data_source)
            #if int(flag) <= int(pages) or next_page[1] != 'next disabled':
            soup = BeautifulSoup(data_source,"lxml")
            jobs_list = soup.find_all(attrs=['job-list'])[0].find_all('li')  #所有招聘信息

            job_url_re = re.compile(r'<a href="(.*?)" ka="job-(\d*)" target="_blank">')
            job_time_re = re.compile(r'<span class="time">(.*?)</span>')
            job_name_re = re.compile(r'<h3 class="name">(.*?)</h3>')
            job_xinzi_re = re.compile(r'<p class="salary">(.*?)-(.*?)</p>')
            job_other_re = re.compile(r'<p>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)</p>')

            for job in jobs_list:
                job_url = job_url_re.findall(str(job))[0][0]  # 每一页的所有职位url
                job_name = job_name_re.findall(str(job))[0]
                job_time = job_time_re.findall(str(job))[0]
                job_xinzi_di = job_xinzi_re.findall(str(job))[0][0]
                job_xinzi_top = job_xinzi_re.findall(str(job))[0][1]
                job_area = job_other_re.findall(str(job))[0][0]
                job_jingyan = job_other_re.findall(str(job))[0][1]
                job_xueli = job_other_re.findall(str(job))[0][2]

                job_dict = {
                    'job_url': job_url,              #
                    'job_name': job_name,            #职位名称
                    'job_time': job_time,            #发布时间
                    'job_xinzi_di': job_xinzi_di,   #最低薪资
                    'job_xinzi_top': job_xinzi_top, #最高薪资
                    'job_area': job_area,            #工作地点
                    'job_jingyan': job_jingyan,      #工作经验
                    'job_xueli': job_xueli           #学历要求
                }
                q.put(job_dict)
                print("%s 放入队列" % job_url)

        except BaseException as zz:
            pass

if __name__ == '__main__':
    start_time = time.time()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 该程序所在目录
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Cache-Control':'max-age=0',
               'Accept-Encoding':'zip, deflate, sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Connection':'keep-alive',
               'Upgrade-Insecure-Requests':'1'
               }
    Base_url = 'http://www.zhipin.com/'

    flag_ip = 1  # 换IP
    flag = 1
    step = 0
    step1 = 1
    start_url = 'http://www.zhipin.com/gongsi/r110874.html'
    data_source1 = requests.get(start_url, headers=headers, timeout=3).text
    total_re = re.compile(r'<b>(\d*)</b>在招职位')
    total = total_re.findall(data_source1)[0]
    pages = int(math.ceil(int(total) / 15) )
    print("共有%s页" % pages)
    print("共%s个职位" % total)

    q = queue.Queue(maxsize=int(total))
    q1 = queue.Queue(maxsize=int(pages))
    for i in range(1,pages+1):
        q1.put(i)
    page_id = 1
    flag = 1
    while int(step) <= int(total) or not q.empty():


        data = requests.get('http://huqinqin.cn/').json()
        print("共获得%s个代理IP" % len(data))
        for pro in data:
            requests_session = requests.session()
            ip = pro['ip']
            port = pro['port']
            proxy_str = 'http://' + str(ip) + ':' + str(port)
            proxies = {"http":proxy_str}
            if not q1.empty() or step <10:
                aa = threading.Thread(target=get_info, args=(proxies,q1.get()))
                aa.start()
                aa.join()

            bb_list = []
            for i in range(10):
                bb = threading.Thread(target=get_job_info, args=(proxies,step,step1))
                bb.start()
                step += 1
                bb_list.append(bb)
                time.sleep(5)
            for bb1 in bb_list:
                bb1.join()
            print("------更换代理IP------")
        print("    重新获取新的代理IP列表     ")

    run_time = time.time() - start_time
    print("All work is Done! 共计爬取%s个职位,耗时%s秒" % (int(step)-int(step1), int(run_time)))
    exit(0)