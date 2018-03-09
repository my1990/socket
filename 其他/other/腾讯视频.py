import requests
from bs4 import BeautifulSoup

def get_tag():
    tag = []
    url = 'https://v.qq.com/'
    tag_data = requests.get(url).content.decode()
    tag_info = BeautifulSoup(tag_data,'lxml')
    tag_list = tag_info.find_all(attrs=['nav_sub_area'])  #data-nav  data-navtitle
    for tag1 in tag_list:
        list = tag1.find_all('a')
        for i in list:
            href = i['href']
            title = str(i.string)
            if title == 'None':
                tag.append(href)   #频道链接
            else:
                print(title,href)
        print('\n')
    return tag

def get():
    url_list = get_tag()
    for url in url_list:
        data = requests.get(url).content.decode()
        soup = BeautifulSoup(data,'lxml')
        list = soup.find_all(attrs=['list_item'])
        for i in list:
            try:
                info = i.find_all('a')[1]
                title = info.string
                href = info['href']
                print(title,href)
                print('\n')
            except BaseException:
                pass


get()