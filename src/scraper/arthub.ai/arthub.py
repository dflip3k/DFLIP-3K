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

#===================================================


def tu(url):

    for i in range(1):
        headers ={}
        headers["Upgrade-Insecure-Requests"]='1'
        headers["User-Agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        html = requests.get(url,headers=headers)

        if html.status_code==200:
            with open(url.split('/')[-1],"wb")as f:
                f.write(html.content)
        else:
            pass


        
def hmtl_content(s,ss):
    for i in range(1):
        headers ={}
        headers["authority"]='fiwduaejmxwtidbnyoxy.supabase.co'
        headers["method"]='GET'
        headers["path"]='/rest/v1/user_art?select=tags%2Cpublic_score%2Cinternal_score%2Chash_id%2Casset_source%2Cid%2Cflag%2Ccreated_by%2Ccreated_by_username%2Cdescription%2Canon_votes_user_art%28user_id%2Cvote%29&flag=is.null&anon_votes_user_art.user_id=eq.64d45cfc-e613-42c6-8563-08d96b4369e9&order=feed_score.desc&offset={0}&limit={1}'.format(s,ss)
        

        headers["scheme"]='https'
        headers["accept"]='*/*'
        headers["accept-encoding"]='gzip, deflate, br'
        headers["accept-language"]='zh-CN,zh;q=0.9'
        headers["accept-profile"]='public'
        headers["apikey"]='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpd2R1YWVqbXh3dGlkYm55b3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzcyNDkxNDIsImV4cCI6MTk5MjgyNTE0Mn0.S4YhWyi5BCPrlD-5HlGf-NV57il_1ucFzWJ7ta6C36w'
        headers["authorization"]='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpd2R1YWVqbXh3dGlkYm55b3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzcyNDkxNDIsImV4cCI6MTk5MjgyNTE0Mn0.S4YhWyi5BCPrlD-5HlGf-NV57il_1ucFzWJ7ta6C36w'
        headers["origin"]='https://arthub.ai'
        headers["prefer"]='count=estimated'
        headers["referer"]='https://arthub.ai/'
        headers["sec-fetch-dest"]='empty'
        headers["sec-fetch-mode"]='cors'
        headers["sec-fetch-site"]='cross-site'
        headers["user-agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        headers["x-client-info"]='supabase-js/2.0.0-rc.8'

        url ='https://fiwduaejmxwtidbnyoxy.supabase.co/'+headers["path"]
        
        html  =requests.get(url,headers=headers)

        return html

def con_open(s):
    
    for i in range(1):
        #      
        headers ={}
        headers["authority"]='fiwduaejmxwtidbnyoxy.supabase.co'
        headers["method"]='GET'
        headers["path"]='/rest/v1/user_art?select=tags%2Cpublic_score%2Cinternal_score%2Chash_id%2Casset_source%2Cid%2Cflag%2Ccreated_by%2Ccreated_by_username%2Cmodel_params%2Cdescription%2Canon_votes_user_art%28vote%29&id=eq.{0}&anon_votes_user_art.user_id=eq.64d45cfc-e613-42c6-8563-08d96b4369e9'.format(s)
        headers["scheme"]='https'
        headers["accept"]='*/*'
        headers["accept-language"]='zh-CN,zh;q=0.9'
        headers["accept-profile"]='public'
        headers["apikey"]='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpd2R1YWVqbXh3dGlkYm55b3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzcyNDkxNDIsImV4cCI6MTk5MjgyNTE0Mn0.S4YhWyi5BCPrlD-5HlGf-NV57il_1ucFzWJ7ta6C36w'
        headers["authorization"]='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpd2R1YWVqbXh3dGlkYm55b3h5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzcyNDkxNDIsImV4cCI6MTk5MjgyNTE0Mn0.S4YhWyi5BCPrlD-5HlGf-NV57il_1ucFzWJ7ta6C36w'
        headers["origin"]='https://arthub.ai'
        headers["prefer"]='count=exact'
        headers["referer"]='https://arthub.ai/art/{0}'.format(s)
        headers["sec-fetch-dest"]='empty'
        headers["sec-fetch-mode"]='cors'
        headers["sec-fetch-site"]='cross-site'
        headers["user-agent"]='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        headers["x-client-info"]='supabase-js/2.0.0-rc.8'

        
        url ='https://fiwduaejmxwtidbnyoxy.supabase.co'+headers["path"]

        html  =requests.get(url,headers=headers)

        body = html.content.decode('utf-8')

        return body

    
def main():
    import pdb;pdb.set_trace()
    for sss in range(0,30*2400,30):
        html =hmtl_content(sss,sss+30)

        con = json.loads(html.text)

        dic = con
        print(sss)
        for i in dic:
            try:
                s =i['id']
                u ='https://arthub.ai/art/'+str(s)
                try:
                    img = 'https://img5.arthub.ai/user-uploads/'+i['asset_source']['uh']+'/'+i['hash_id']+'/'+i['asset_source']['files'][0]
                except:
                    img = 'https://img6.arthub.ai/'+i['asset_source']['file']

                description = i['description']

                try:
                    v = data[s]
                    print('已有')
                except:
                    print(u)
                    html = con_open(s)
                    text =json.loads(html)[0]
                    text = text['model_params']
                    print(u,'已下载')
                    time.sleep(3)
                    data[s]=[u,img,text,description]
                    cun('data1')
            except:
                # import pdb;pdb.set_trace()
                print('error {}'.format(sss))
            
if __name__ == '__main__':

    data=data_open('./data1')
    main()
    # excel()
    # data={}
    # cun('./data')