# coding=utf-8
import re
import string
from io import BytesIO

import pytesseract
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup


def login():
    login_url = 'http://www.ztt88.cn/member.php?mod=logging&action=login'
    session = requests.Session()
    req = session.get(login_url)
    login_page = req.content
    login_soup = BeautifulSoup(login_page, "lxml")
    formhash_tag = login_soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']
    print formhash
    params = {
        "fastloginfield": "username",
        "password": 'yj123456',
        "quickforward": "yes",
        "handlekey": "ls",
        "username": 'yyyjjj',
    }
    req = session.post(
        'http://www.ztt88.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1',
        data=params)
    auth = re.search(r'auth=(.*?)&', req.content).group()

    url_auth = 'http://www.ztt88.cn/member.php?mod=logging&action=login&' + auth + 'referer=http%3A%2F%2Fwww.ztt88.cn%2Fforum.php&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    req = session.get(url_auth)

    idhash = re.search(r'updateseccode(.*?),', req.text).group()[15:-2]
    print idhash

    req = session.get(
        'http://www.ztt88.cn/misc.php?mod=seccode&action=update&idhash=' + idhash + '&0.7016755747032235&modid=undefined')
    # print req.content
    url_img = re.search(r'src="misc\.php\?mod=seccode&(.*?)"', req.content).group()
    url_img = 'http://www.ztt88.cn/' + url_img[5:-1]
    print url_img

    headers = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Connection': 'keep-alive',
               'Host': 'www.ztt88.cn',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
               'Referer': 'http://www.ztt88.cn/misc.php?mod=seccode&action=update&idhash=' + idhash + '&0.7016755747032235&modid=undefined'}
    req = session.get(url_img, headers=headers)
    with open('picture.png', 'wb') as file:
        file.write(req.content)
    img = extract_image(req.content)  ##获取图像数据
    captcha = ocr(img)  ##利用OCR进行识别图像内文本
    print captcha

    secverify_url = 'http://www.ztt88.cn/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=' + idhash + '&secverify=' + captcha
    req = session.get(secverify_url)
    print req.content
    print auth
    params = {
        "formhash": formhash,
        "seccodeverify": captcha,
        "seccodehash": idhash,
        "referer": "http://www.ztt88.cn/forum.php",
        "seccodemodid": 'member::logging',
        "loginfield": "username",
        "password": 'yj123456',
        "username": 'yyyjjj',
        "questionid": '0',
        "answer": "",

    }
    print params
    finish_url = 'http://www.ztt88.cn/member.php?mod=logging&action=login&loginsubmit=yes&inajax=1'
    req = session.post(finish_url, data=params, headers=headers)

    # print session.get('http://www.ztt88.cn/forum.php?mod=post&action=newthread&fid=64').content.decode('gbk')

    post_tie_url = 'http://www.ztt88.cn/forum.php?mod=post&action=newthread&fid=64&extra=&topicsubmit=yes'
    req = session.get('http://www.ztt88.cn/forum.php?mod=post&action=newthread&fid=64')
    # print req.content.decode('gbk')
    headers = {'Referer': 'http://www.ztt88.cn/forum.php?mod=post&action=newthread&fid=64',
               'Upgrade-Insecure-Requests': '1',
               'Origin': 'http://www.ztt88.cn',
               'Host': 'www.ztt88.cn',
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    login_soup = BeautifulSoup(req.content, "lxml")
    formhash_tag = login_soup.find('input', attrs={'name': 'formhash'})
    formhash = formhash_tag['value']
    print formhash
    posttime = str(int(time.time()))
    subject = '成功发帖'
    subject = subject.decode('utf-8').encode('gbk')
    message = """
    【伊人住址】：sss
    【逍遥时间】：
    【伊人昵称】：
    【伊人简介】：dasda
    【伊人特点】：
    【享受项目】：
    【逍遥价格】：dasda
    【逍遥环境】：
    【逍遥细节】：
    【事后感受】：
    【综合打分】：
    【联系方式】：[hide]隐藏内容 Abc[/hide]
    【伊人照片】：[hide]隐藏内容 Abc[/hide]"""
    message = message.decode('utf-8').encode('gbk')
    data = { "formhash": formhash,
              'wysiwyg': "1",
              'subject': subject,
              'message': message,
              'allownoticeauthor': "1",
              'usesig': "1",
              'save': ""}
    print data
    req = session.post(post_tie_url, data=data, headers=headers)
    print req.content.decode('gbk')

def extract_image(img_data=None):
    ##利用逗号分割，将其分为两部分，移除该前缀。这是一张进行了base64编码的图像
    # open('test_.png', 'wb').write(data.decode('base64'))
    ##进行base64解码，回到最初的二进制

    # binary_img_data = img_data.decode('base64')
    ##要想加载该图片，PIL需要对一个类似文件的接口，在传给Image类，我们又使用ByteIO对这个二进制进行封装
    # file_like = BytesIO(binary_img_data)
    img = Image.open('picture.png')
    return img

def ocr(img):
    # threshold the image to ignore background and keep text
    img_array = img.load()
    num = {}
    print img.size
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            L = img_array[i, j][0] * 299 / 1000 + img_array[i, j][1] * 587 / 1000 + img_array[i, j][2] * 114 / 1000
            if L in num:
                num[L] += 1
            else:
                num[L] = 1
    num = sorted(num.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    print num
    max_num = num[0][0]
    gray = img.convert('L')
    #gray.save('captcha_greyscale.png')
    bw = gray.point(lambda x: 0 if x >= max_num - 3 and x <= max_num + 3 else 255, '1')
    bw.save('captcha_threshold.png')
    word = pytesseract.image_to_string(bw)
    print word
    return word



if __name__ == '__main__':
    login()

