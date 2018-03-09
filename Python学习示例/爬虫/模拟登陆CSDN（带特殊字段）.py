from urllib import request
import re
import requests
url = 'http://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'

souce = request.urlopen(url).read().decode()  #获取网站源码
def get_lt():  #该参数为每个需要登录的用户的一个流水号。
    lt_re = re.compile(r'value="(LT-\d*-\w{30})"')
    lt = lt_re.findall(souce)
    return lt
def get_execution():
    execution_re = re.compile(r'<input type="hidden" name="execution" value="(\w*)" />')
    execution = execution_re.findall(souce)
    return execution
def get_eventId():
    eventId_re = re.compile(r'<input type="hidden" name="_eventId" value="(\w*)" /> ')
    eventId = eventId_re.findall(souce)
    return eventId

def login_csdn(username,password):
    data = {'username': username,
            'password': password,
            'lt':get_lt(),
            'execution':get_execution(),
            '_eventId':get_eventId(),
            }
    #print('lt:',get_lt(),'\nexecution:',get_execution(),'\n_eventId:',get_eventId())
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    headers = {'User_Agent': user_agent}
    request_session = requests.Session()
    login = request_session.post(url, data=data, headers=headers)
    print(login)

    people = request_session.get(url='http://my.csdn.net/my/mycsdn', headers=headers).text
    print(people)


    re2 = re.compile(r'<a href="/my/follow" target="_blank">(\d*)</a>')
    follow = re2.findall(people)



if  __name__ == '__main__':
    username = input("username:")
    password = input("password:")
    login_csdn(username,password)














