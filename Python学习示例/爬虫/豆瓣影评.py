import requests,time
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/subject/5350027/comments?status=P'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
def get_info():
    movie_info = []  #电影信息，导演 演员 等信息
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text,'lxml')
    title = soup.title.string  #电影名
    attrs_info = soup.find_all(attrs=['attrs'])[0]
    attrs_info1 = attrs_info.find_all('p')
    for attrs in attrs_info1:
        movie_info.append(str(attrs.text).strip().lstrip().replace('\n','').replace(' ',''))

    look = str(soup.find_all(attrs=['fleft CommentTabs'])[0].text).strip().lstrip().replace('\n',' ')  #多少人看过，多少人想看
    comment_percent = str(soup.find_all(attrs=['comment-filter'])[0].text).strip().lstrip()[2:].strip().replace('\n',' ') #好评 差评
    #print(data.text)
    return title

def get_pingjia():
    id = 0
    title = get_info()
    f = open(title+'.txt','a',encoding='utf-8')
    while title != '没有访问权限':
        pingjia_url = url + '&limit=20&sort=new_score&percent_type=&start=' + str(id)
        pingjia_data = requests.get(pingjia_url,headers=headers)
        soup1 = BeautifulSoup(pingjia_data.text, 'lxml')
        title = soup1.title.text
        pingjia_list = soup1.find_all(attrs=['comment-item'])
        for pingjia in pingjia_list:
            pingjia_str = str(pingjia.find(attrs=['comment']).p.string) + '\n'
            f.write(pingjia_str)
            print(pingjia_str)
            time.sleep(3)
        id += 20
    else:
        print(pingjia_url)
        print(title)
        f.close()
get_pingjia()
#get_info()
