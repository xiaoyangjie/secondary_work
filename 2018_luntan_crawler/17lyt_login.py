# coding=utf-8
import requests
from bs4 import BeautifulSoup
from lxml import etree

def login(pwd='wsnimm22', user='花花世界22'):
    login_url = 'http://www.17lyt.com/member.php?mod=logging&action=login'
    session = requests.Session()
    loginpage = session.get(login_url).text
    login_soup = BeautifulSoup(loginpage, "lxml")
    formhash_tag = login_soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']
    print formhash
    user = user.decode('utf-8').encode('gbk')
    params = {
        "answer": "",
        "formhash": formhash,
        "loginfield": "username",
        "password": pwd,
        "questionid": "0",
        "referer": "http://www.17lyt.com/plugin.php?id=dsu_paulsign:sign",
        "username": user,
    }

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    req = session.post(
        'http://www.17lyt.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LQ161&inajax=1',
        data=params)

    display_url = 'http://www.17lyt.com/thread-278975-1-1.html'
    req = session.get(display_url)
    # print req.content.decode('gbk')

    login_soup = BeautifulSoup(req.content, "lxml")
    formhash_tag = login_soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']
    print formhash

    post_url = 'http://www.17lyt.com/forum.php?mod=post&action=reply&fid=145&tid=278975&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
    params = {'message': 'woshishui haha kankan',
              'formhash': formhash,
              'usesig': "",
              'subject': ""}
    # req = session.post(post_url, data=params)

    req = session.get(display_url)
    html = etree.HTML(req.content)

    flag = 0
    # print req.content.decode('gbk')
    for i in html.xpath('//td[@class="t_f"]/text()'):
        i = i.encode('utf-8')

        if flag != 0 and i != ' ':
            print i
            flag = 0
        if '妹妹住址' in i:
            print i.split('：')[1]
        if '约会时间' in i:
            print i.split('：')[1]
        if '妹妹简介' in i:
            print i.split('：')[1]
        if '妹妹姓名' in i:
            print i.split('：')[1]
        if '妹妹特点' in i:
            print i.split('：')[1]
        if '享受项目' in i:
            print i.split('：')[1]
        if '约会价格' in i:
            print i.split('：')[1]
        if '约会环境' in i:
            print i.split('：')[1]
        if '约会细节' in i:
            print i.split('：')[1]
        if '综合打分' in i:
            print i.split('：')[1]
        if '联系方式' in i:
            flag = 1
        if '妹妹照片' in i:
            print i.split('：')[1]
    for i in html.xpath('//ignore_js_op/img/@zoomfile'):
        print i

if __name__ == '__main__':
    login()