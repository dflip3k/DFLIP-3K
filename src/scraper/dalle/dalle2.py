from PIL import Image
import requests
import json
from urllib.request import quote
import time
import re
from bs4 import BeautifulSoup as bs
import pickle
import openpyxl
from openpyxl import load_workbook
import string,random
import cv2  
import numpy as np
    
def cun(s):
    file = open(s,'wb')
    pickle.dump(data,file)
    file.close()

def data_open(s):
    file = open(s,'rb')
    data = pickle.load(file)
    file.close()
    return data

def rr(word):

    
    word = re.sub(' ','',word)
    word = re.sub('\?','',word)
    word = re.sub('\n','',word)
    word = re.sub('\t','',word)
    word = re.sub('\xa0','',word)
    word = re.sub('\r','',word)
    word = re.sub('\u3000','',word)
    word = re.sub(r'<p>','',word)
    word = re.sub(r'</p>','',word)
    word = re.sub(r'&nbsp;','',word)


    return word

def xie():

    with open("数字.txt","w",encoding='utf-8')as f:

        f.write(str(html))

        
def az(s):

    u =[]

    for i in range(ord("A"),ord("Z")+1):
        u.append(chr(i))
        if len(u)==s:
            return u
        else:
            pass

    for ii in range(ord("A"),ord("Z")+1):

        for i in range(ord("A"),ord("Z")+1):
            u.append(chr(ii)+chr(i))
            if len(u)==s:
                return u
            else:
                pass
def excel():

    wb = openpyxl.Workbook()
    word = wb.active
    
    for i in range(len(data)):

        a = az(len(data[i]))
        for r in range(len(a)):
            
            su = a[r]+str(i+1)
            word[su]=data[i][r]
            print(data[i][r])

    a = '搜索结果'
    wb.save('{0}.xlsx'.format(a))
    print('已完成，已保存好了')
         

def ha():

    aa = a.split('\n')
    headers ={}
    print("headers ={}")
    for i in aa:
        e = i.split(': ')
        print('headers["{0}"]'.format(e[0])+'='+"'{0}'".format(e[1]))

#        requests.packages.urllib3.disable_warnings() 忽略警告

#        html = requests.get(url,headers=headers,verify=False)  verify=False https证书关闭

#===================================================


def tu(url):

    for i in range(1):
        headers ={}
        headers["Upgrade-Insecure-Requests"]='1'
        headers["User-Agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        requests.packages.urllib3.disable_warnings()

        html = requests.get(url,headers=headers,verify=False)

        if html.status_code==200:
            with open(url.split('/')[-1]+".webp","wb")as f:
                f.write(html.content)
        else:
            pass
        



def hmtl_content(y):
    for i in range(1):

        headers ={}
        headers["Accept"]='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        
        headers["Accept-Language"]='zh-CN,zh;q=0.9'
        headers["Cache-Control"]='max-age=0'
        headers["Connection"]='keep-alive'
        headers["Host"]='dalle2.gallery'
        headers["Sec-Fetch-Dest"]='document'
        headers["Sec-Fetch-Mode"]='navigate'
        headers["Sec-Fetch-Site"]='none'
        headers["Sec-Fetch-User"]='?1'
        headers["Upgrade-Insecure-Requests"]='1'
        headers["User-Agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

        
        url ='https://dalle2.gallery/api/images/aggregated?pagesize=20&page={0}'.format(y)
        requests.packages.urllib3.disable_warnings()
        html  =requests.get(url,headers=headers, verify=False)


        return html

def con_open(url):
    
    for i in range(1):
        #      
        headers ={}
        headers["Accept"]='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        headers["Accept-Encoding"]='gzip, deflate, br'
        headers["Accept-Language"]='zh-CN,zh;q=0.9'
        headers["Connection"]='keep-alive'
        headers["Host"]='dalle2.gallery'
        headers["Sec-Fetch-Dest"]='document'
        headers["Sec-Fetch-Mode"]='navigate'
        headers["Sec-Fetch-Site"]='none'
        headers["Upgrade-Insecure-Requests"]='1'
        headers["User-Agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

        requests.packages.urllib3.disable_warnings()
        html  =requests.get(url,headers=headers, verify=False)

        return html

    
def main():
    import pdb;pdb.set_trace()
    for s in range(1636,5000):
        print("page: {}".format(s))
        try:
            html =hmtl_content(s)

            dic = json.loads(html.text)

            for i in dic:

                for e in range(1):
                    u ='https://dalle2.gallery/api/images/'+i['Ids'][0]
                    text= i['Caption']
                    img = 'https://ditlgf0hrcl4j.cloudfront.net/'+i['Ids'][0]+'/generated'

                    #tu(img)   #这个函数会下载图片

                if [u,img,text] in data:
                    print('已有')
                else:
                    data.append([u,img,text])
                    # print(u)
                    # print(img)
                    # print(text)
                    print(u,'已下载')

            time.sleep(5)
        except:
            print("error")
        cun('dalle2')

    #excel()  #这个函数会生成表格
    cun('dalle2')

            
if __name__ == '__main__':
    data=data_open('dalle2')
    main()