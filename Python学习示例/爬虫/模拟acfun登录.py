from urllib import request
import re
import requests
request_session = requests.Session()  #会话对象requests.Session能够跨请求地保持某些参数，比如cookies，即在同一个Session实例发出的所有请求都保持同一个cookies,而requests模块每次会自动处理cookies，这样就很方便地处理登录时的cookies问题
date = {'username':'15257158293','password':'csbt34.'}
url = 'http://www.acfun.cn/login.aspx'
post = request_session.post(url, data=date).json()
print(post)
member = request_session.get(url="http://www.acfun.cn/member").text #返回的是Unicode型的数据，也就是说，如果你想取文本，可以通过r.text
member1 = request_session.get(url="http://www.acfun.cn/member").content #返回的是bytes型也就是二进制的数据，如果想取图片，文件，则可以通过.content

re1 = re.compile('<a href="#area=banana"><span class="pts">(\d*)</span><span class="hint">香蕉</span></a>')
banner = re.findall(re1,member)
print(banner[0])
requests.pac




