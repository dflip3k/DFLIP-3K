
# url='https://finding.art/#/?prompt='

import base64
from Crypto.Util.Padding import unpad,pad
from Crypto.Cipher import AES
from hashlib import md5
import requests
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor#导入线程池

path='img'#创建的文件夹


# py时间戳和js时间戳
t_python=str(time.time()).rsplit(".")[0]
t_js=str(int(time.time()*1000))



# def md5_encrypt():
n = "FJFxjMY9B$PHXcx^bRot@3%Ya7e78d43"
o=n+t_js
#md5加密
obj=md5()
obj.update(o.encode('utf-8'))
authority_info=obj.hexdigest()


def reques(pageId):
    params={
        "_t": t_python,#时间戳
        "topic": "",
        "pageId": pageId,
        "pageSize": "50",
    }
    if pageId==1:
        params["pageSize"]="30"
    url='https://finding.art/api/image/v1/discover'
    headers={
        "authority-info": authority_info,
        "authority-time": t_js,
        "referer": "https://finding.art/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    }
    respon=requests.get(url=url,headers=headers,params=params,timeout=10)
    data=respon.json()['data']
    return data


# 解密
def decrypt(e):
    key=b"O1@7nvYjO&N2dbhfoF1P2hCJiMlmgZ0K"#m
    iv=b"uoqQxR%eRTtxYqdk"#A  MODE_CBC  -> 需要IV(偏移量)
    aes=AES.new(key=key, iv=iv,mode=AES.MODE_CBC)#创建解密器
    result = aes.decrypt(base64.b64decode(e))  # 这里只能解密字节
    r = unpad(result, 16)
    data=r.decode("utf-8")
    return data


def download_reques(id):
    img_path = os.path.join(path + '//' + id)
    if os.path.exists(img_path):
        print('文件已存在'+id)
    else:
        headers = {
            "authority-info": authority_info,
            "authority-time": t_js,
            "referer": "https://finding.art/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        }
        params = {
            "_t": t_python,
            "id": str(id),
            "pageId": "1",
            "pageSize": "50"
        }
        two_url = 'https://finding.art/api/image/v1/series'
        respon = requests.get(url=two_url, headers=headers, params=params, timeout=4)
        data = respon.json()['data']
        data = decrypt(data)
        data = json.loads(data)
        lis = data["list"]
        mkdir(img_path)
        for l in lis:
            with open(img_path + '//' + id + '.txt', 'a+', encoding='utf-8') as f:
                f.write((str(l) + '\r\n'))
                f.close()
            imageUrl = l["imageUrl"]
            download_headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
            }
            name = imageUrl.split('/')[-1] + '.png'
            img_respon = requests.get(url=imageUrl, headers=download_headers, timeout=2)
            with open(img_path + '//' + name, 'wb') as f:
                f.write(img_respon.content)
                f.close()
            print('已保存' + name)



def mkdir(path):#判断文件夹是否存在  不存在就新建
    # os.path.exists 函数判断文件夹是否存在
    folder = os.path.exists(path)
    # 判断是否存在文件夹如果不存在则创建为文件夹
    if not folder:
        # os.makedirs 传入一个path路径，生成一个递归的文件夹；如果文件夹存在，就会报错,因此创建文件夹之前，需要使用os.path.exists(path)函数判断文件夹是否存在；
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print('文件夹创建成功：', path)
        # print('\n')
    else:
        print('文件夹已经存在：', path)
        # print('\n')



def main():
    mkdir(path)
    pool = ThreadPoolExecutor(8)
    for pageId in range(1,10000):#爬取页数
        print(pageId)
        data=reques(pageId)
        data=decrypt(data)
        lis = json.loads(data)['list']
        ids=[]
        for li in lis:
            id = li['id']
            ids.append(id)
        pool.map(download_reques, ids)



if __name__ == '__main__':
    main()
