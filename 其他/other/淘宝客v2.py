#-*- coding: UTF-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from urllib import parse
import webbrowser
now_time = int(time.time())

class quan:
    def __init__(self,url):
        self.url = url
        self.id = id
    def quan(self,sour_url1):
        sour_url = sour_url1
        id = re.findall(r'id=(\d{7,19})',sour_url)[0]
        try:
            data = requests.get(sour_url).text
            soup = BeautifulSoup(data,'lxml')
            title_taobao = soup.find_all(attrs=["tb-main-title"]) #淘宝规则
            title_tianmao = soup.find_all(attrs=['tb-detail-hd'])  #天猫规则
            #print('title_taobao', title_taobao)
            # print('title_tianmao', title_tianmao)
            if len(title_taobao) == 0:   #匹配不到，说明是天猫网站
                title = title_tianmao[0].find_all('h1')[0].text.strip()
                #print('title2', title)
            else:
                title = soup.find_all('h3')[0].text.strip()  # 淘宝规则
                #print('title3', title)

            url = 'http://quanhoufan.cc/app/index.php?i=3&c=entry&do=index&m=bsht_tbkquan&keyword='+ parse.quote(title) \
                  + '&itemid=' + str(id)+ '&itemfee=&itempic=&sid=&shopid=&actid=&t='+str(now_time)
            print('转换后的网址',url)   #最终网址
            url2 = 'http://quanhoufan.cc/app/index.php?i=3&c=entry&shopid=0&itemid='+str(id)+ '&actid=&do=getxtkinfo&m=bsht_tbkquan'
            #print('url2',url2)
            data2 = requests.get(url2).json()['nb_qlist']
            #print('data2',data2)
            nb_dict = {}
            itemfee = data2['itemfee']  #原价
            if 'itemfee2' in data2:
                itemfee2 = data2['itemfee2'] #券后价
            else:
                itemfee2 = itemfee
            itempic = data2['itempic'] #商品图片链接
            maijia_id = data2['maijia_id'] #卖家id
            title = data2['title']  #商品名称
            qfee = str(data2['yhjfee'])   #券
            if qfee == 'None':
                qfee = 0

            f1 = data2['fl']       #约奖
            itemmsell = data2['itemmsell']  #已售
            itemyhj_yl = data2['itemyhj_yl']  #剩余券数
            href = data2['href']    #商品链接
            nb_dict['原价'] = itemfee
            nb_dict['券后价'] = itemfee2
            nb_dict['商品名称'] = title
            nb_dict['优惠券'] = qfee
            nb_dict['约奖'] = f1
            nb_dict['商品链接'] = href
            nb_dict['图片链接'] = itempic
            nb_dict['已售'] = itemmsell
            nb_dict['剩余'] = itemyhj_yl
            print(nb_dict)
            f = open('样式.html','r',encoding='utf-8')
            data2 = f.read()
            soup1 = BeautifulSoup(data2,'lxml')
            f.close()
            #print(soup1.find_all(attrs='pict_src')[0]['href'])
            #print(data2)
            soup1.find_all(attrs=['picture'])[0]['src'] = itempic #修改图片链接
            soup1.find_all(attrs=['title'])[0].string = title #修改标题
            soup1.find_all(attrs=['qfee'])[0].string = '优惠券：%s        返利：%s'% (round(itemfee-itemfee2,2),round(int(f1)/100,3)) #修改优惠券
            soup1.find_all(attrs=['itemfee2'])[0].string = "到手价 ￥%s "% round(itemfee-int(qfee)-(int(f1)/100),3)#修改到手价
            soup1.find_all(attrs=['pict_src'])[0]['href'] = href  #修改商品链接
            # print(soup1.find_all(attrs=['picture'])[0]['src'])
            # print(soup1.find_all(attrs=['title'])[0].string)   # 修改标题
            # print(soup1.find_all(attrs=['qfee'])[0].string)
            # print(soup1.find_all(attrs=['itemfee2'])[0].string)
            f1 =open('样式-%s.html'% id,'w',encoding='utf-8')
            f1.write(str(soup1))
            f1.close()
            webbrowser.open('样式-%s.html' % id)
        except BaseException as e:
            print(e)
            print("网络异常，请再次尝试~")


        ###################以下是获取所以商品信息######################
        # 商品json
        # result_url = 'http://quanhoufan.cc/app/index.php?i=3&c=entry&shopid=0&stype=0&type=0&do=gethdinfo&m=bsht_tbkquan&q=' + parse.quote(
        #     title) + '&limit=1'
        # # print(result_url)
        # nb_qlist1 = requests.get(result_url).json()
        # print(nb_qlist1)
        # if nb_qlist1['num'] == 1:  #商品列只有一个的时候
        #     print("只有一个商品")
        #     nb = nb_qlist1['nb_qlist']
        #     nb_dict = {}
        #     itemfee = nb['itemfee']  #原价
        #     itemfee2 = nb['itemfee2'] #券后价
        #     itemid = nb['itemid']  #商品id
        #     itempic = nb['itempic'] #商品图片链接
        #     maijia_id = nb['maijia_id'] #卖家id
        #     title = nb['title']  #商品名称
        #     qfee = nb['qfee']   #券
        #     nb_url = nb['url']   #商品链接
        #     f1 = nb['fl']
        #     nb_dict['原价'] = itemfee
        #     nb_dict['券后价'] = itemfee2
        #     nb_dict['商品名称'] = title
        #     nb_dict['优惠券'] = qfee
        #     nb_dict['约奖'] = f1
        #     print(nb_dict)
        # else:
        #     print("发现%s件商品,信息分别如下：" % len(nb_qlist1['nb_qlist']))
        #     for nb in nb_qlist1['nb_qlist']:
        #         #print(nb)
        #         nb_dict = {}
        #         itemfee = nb['itemfee']  #原价
        #         itemfee2 = nb['itemfee2'] #券后价
        #         itemid = nb['itemid']  #商品id
        #         itempic = nb['itempic'] #商品图片链接
        #         maijia_id = nb['maijia_id'] #卖家id
        #         title = nb['title']  #商品名称
        #         qfee = nb['qfee']   #券
        #         nb_url = nb['url']   #商品链接
        #         f1 = nb['fl']
        #         nb_dict['原价'] = itemfee
        #         nb_dict['券后价'] = itemfee2
        #         nb_dict['商品名称'] = title
        #         nb_dict['优惠券'] = qfee
        #         nb_dict['约奖'] = f1
        #         print(nb_dict)
        ###################以上是获取所以商品信息######################


if __name__ == "__main__":
    #url1 = 'https://item.taobao.com/item.htm?id=556385184326&_u=t2dmg8j26111'    #淘宝  手机壳
    #url1 = 'https://item.taobao.com/item.htm?id=528694002391&_u=t2dmg8j26111'   #淘宝  化妆品
    #url1 = 'https://detail.tmall.com/item.htm?id=35613509507&_u=t2dmg8j26111'  #天猫   内衣
    #url1 = 'https://detail.tmall.com/item.htm?spm=a1z10.4-b-s.w5003-16257934302.1.20cc225fTd9ECh&id=552462891236&scene=taobao_shop'  #天猫 裙子
    url1 = input("输入网址>>:")
    s = str(url1).strip()
    quan(s)

