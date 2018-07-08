#coding=utf-8

import  os
import urllib2
from lxml import etree
from multiprocessing import Process
import  requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = "U2FsdGVkX19YqERXMHH8vaMY9PaM6PTlgOcirdqXncY6+6Nm2NUxAJX1gMquqJBk"
url_2 = "U2FsdGVkX1896Im78FP7S3eUW5rCmvtM8mRAIaG9mKMVfVVjwhYfv2/8CwnxDt6w"
url_index = "U2FsdGVkX1/IyfpGJXnejiywjG0Co3AgDjgJRNTtw0zEkB/BDNA7XVYbplSJPMbXU/KQBNFTSLwp89m8vrT6zA=="


doc = {1:"pic1", 2:"pic2", 3:"pic3"}

#Url use AES decode will be a surprise    http://tool.chinaz.com/Tools/textencrypt.aspx

def http(url):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": "__cfduid=d22e812d123d57205a0b24a16ba488e561530969763",
        "referer": url_index,
        "user-agent": "Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    request = urllib2.Request(url, headers=headers)
    html = urllib2.urlopen(request).read()

    return html

def menu():

    listUrl = []
    for num in [1, 2, 3]:
        full_url = url + "piclist" + str(num) + "/"
        listUrl.append(full_url)
    menuNum = []
    num = 0
    while True:
        num = int(raw_input("Please input ： \n"))
		#Input 0 to start downloading
        if num == 0:
            break
        menuNum.append(num)

    for i in menuNum:
        p = Process(target=spider, args=(doc, listUrl, i))
        p.start()


def spider(doc, listUrl, num):
    if num > 4:
        fullNum = num -2
    else:
        fullNum = num -1

    needUrl= listUrl[fullNum]
    print "Starting--->>>",
    print doc[int(num)],
    print needUrl
    print num
    loadPage(needUrl, num)

def loadPage(needUrl, num):
    html = http(needUrl)
    content = etree.HTML(html)
    full_name = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/text()')
    full_url = content.xpath('//div[@class="mainArea"]/ul[@class]/li/a/@href')
    listImgName = []
    listImgUrl = []
    for content in full_name:
        listImgName.append(content)
    for content in full_url:
        listImgUrl.append(url_2 + content)

    makeDir(listImgName, num)
    loadImage(listImgUrl, listImgName, num)

def loadImage(listImgUrl, listImgName, num):
    i=0
    for content in listImgUrl:
        html = http(content)
        content = etree.HTML(html)
        listImgSrc = content.xpath('//div[@class="picContent"]/img/@src')
        #print imgSrc
        writePage(listImgSrc, listImgName[i], num)
        i += 1

def makeDir(list, num):
    path = ("D:/kankan/" + doc[num]).decode("utf-8")

    if not os.path.exists(path):
        os.mkdir(path)

    #for text in list:
        #fullPath = path + "/" + text
        #if not os.path.exists(fullPath):
            #os.mkdir(fullPath)

def writePage(listImgSrc, imgFolder, num):
    for imgUrl in listImgSrc:
        print "Downloading：" + imgUrl
        #path = ("D:/kankan/" + doc[num] + "/" + imgFolder).decode("utf-8")
        path = ("D:/kankan/" + doc[num]).decode("utf-8")
        imgPath = path + "/" + imgUrl.split('/')[-1]
        if not os.path.exists(imgPath):
            response = requests.get(imgUrl)
            response.raise_for_status()
            with open(imgPath, 'wb') as f:
                f.write(response.content)

def main():
    for num in [1, 2, 3]:
        print num,doc[num]
    menu()

if __name__ == '__main__':
    main()