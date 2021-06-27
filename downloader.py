# -*- encoding: utf-8 -*-
'''
@File    :   downloader.py
@Time    :   2021/06/27 10:24:10
@Author  :   olixu 
@Version :   1.0
@Contact :   273601727@qq.com
@WebSite    :   https://blog.oliverxu.cn
'''

# here put the import lib
import os
import sys
import time
import argparse
import random
import json
import shutil
from collections import defaultdict
from urllib.parse import quote
import requests
from lxml import etree
import fitz
import pdb

# To DO list
# 1. 可以抓取元数据信息
# 2. 进行选择抓取多少个page的pdf数据
# 3. 

def main():
    """
    下载学位论文入口程序：

    调用方式：python downloader.py --pages '1-2' --major '计算机'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=str, required=True)    #   
    parser.add_argument('--choose_key', type=str, required=True) # 1.主题(topic) 2.题名() 3.关键词() 4.作者() 5.院系 6.(专业) 7.(导师) 8.(年份)
    parser.add_argument('--xuewei', type=str, required=True) # 0：硕博论文 1：博士论文 2：硕士论文
    parser.add_argument('--px', type=str, required=True) # 1：按题名字顺序排序 2：按学位年度倒排序
    parser.add_argument('--page', type=str, required=True)  # 希望抓取多少页的数据，一页的元数据是20篇论文
    args = parser.parse_args()

    info_url = "http://thesis.lib.sjtu.edu.cn/sub.asp?content={}&choose_key={}&xuewei={}&px={}&page=".format(quote(args.content), args.choose_key, args.xuewei, args.px)
    pages = args.page.split('-')
    pages = [int(pages[0]), int(pages[1])]
    papers = download_main_info(info_url, pages)
    pdb.set_trace()
    jpg_dir = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "".join(random.sample('zyxwvutsrqponmlkjihgfedcba23429837498234',5))
    for paper in papers:
        print(100*'@')
        paper_filename = paper['year'] + '_' + paper['filename'] + '_' + paper['author'] + '_' + paper['mentor'] + '.pdf'
        if verify_name(paper_filename):
            print("论文{}已经存在".format(paper_filename))
            continue
        print(paper_filename)
        print(paper)
        print("正在下载论文：", paper['filename'])
        print(paper['filename'])
        #sys.exit()
       # jpg_dir = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
        init(jpg_dir=jpg_dir)
        try:
            download_jpg(paper['link'], jpg_dir=jpg_dir)
            merge_pdf(paper_filename, jpg_dir=jpg_dir)
        except:
            pass

def verify_name(paper_filename):
    if paper_filename in os.listdir('./papers'):
        return True
    return False

def init(jpg_dir):
    """初始化文件夹路径
    """
    try:
        shutil.rmtree('./{}/'.format(jpg_dir))
        print("删除本地{}文件夹".format(jpg_dir))
    except Exception as e:
        print(e)
    try:
        os.mkdir('./{}/'.format(jpg_dir))
        print("新建本地{}文件夹".format(jpg_dir))
    except Exception as e:
        print(e)

def download_main_info(info_url: str, pages: list):
    papers = []
    info_url = info_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    result = requests.Session()
    for page in range(pages[0], pages[1]+1):
        print("正在抓取第{}页的info".format(page))
        info_url_construction = info_url + str(page)
        response = result.get(info_url_construction, headers=headers, allow_redirects=False)
        html = etree.HTML(response.content, etree.HTMLParser())
        for i in range(2, 22):
            # 有些是论文保密，所以link需要错误处理
            info_dict = defaultdict(str)
            try:
                filename = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]//td[2]/text()'.format(i))[0]
                author = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[3]/div/text()'.format(i))[0]
                mentor = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[6]/div/text()'.format(i))[0]
                year = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[8]/div/text()'.format(i))[0]
                link = "http://thesis.lib.sjtu.edu.cn/" + html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[9]/div/a[2]/@href'.format(i))[0]
                info_dict['filename'] = filename
                info_dict['author'] = author
                info_dict['mentor'] = mentor
                info_dict['year'] = year
                info_dict['link'] = link
                papers.append(info_dict)
            except Exception as e:
                print(e)
    print("总共抓取到{}个元数据信息".format(len(papers)))
    return papers

def download_jpg(url: str, jpg_dir: str):
    """下载论文链接为jpg
        :param url: 阅读全文链接
    """
    url = url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    result = requests.Session()
    print("开始获取图片地址")
    response = result.get(url, headers=headers, allow_redirects=False)
    #print(response.content)
    #print(response.status_code)
    #print(response.headers['Location'])
    url = response.headers['Location']
    response = result.get(url, headers=headers, allow_redirects=False)
    #print(response.content)
    #print(response.status_code)
    #print(response.headers['Location'])
    url = response.headers['Location']
    response = result.get(url, headers=headers, allow_redirects=False)
    #print(response.content)
    #print(response.status_code)
    #print(response.headers['Location'])
    url_bix = response.headers['Location'].split('?')[1]
    url = "http://thesis.lib.sjtu.edu.cn:8443/read/jumpServlet?page=1&" + url_bix
    #print(url)
    response = result.get(url, headers=headers, allow_redirects=False)
    #print(response)
    #print(response.content)
    #print(type(response))
    #print(type(response.content))
    #print(json.loads(response.content.decode()))
    urls = json.loads(response.content.decode())
    #print(urls['list'][0]['src'])
    #print(urls.keys())
    print("已经获取到图片地址")
    i = 1
    while(True):
        #print("在while循环里")
        fig_url = "http://thesis.lib.sjtu.edu.cn:8443/read/" + urls['list'][0]['src'].split('_')[0] + "_{0:05d}".format(i) + ".jpg"
        #print(fig_url)
        response = result.get(fig_url, headers=headers).content
        #print(response.content)
        #print(response)
        #print(type(response))
        #print(len(response))
        while len(response) < 2000 and len(response) != 1049:
            response = result.get(fig_url, headers=headers).content
            time.sleep(1)
        if len(response) == 1049:
            print(response)
            break
        with open('./{}/{}.jpg'.format(jpg_dir, i), 'wb') as f:
            f.write(response)

        i = i + 1
        print(i)
        time.sleep(1)

def merge_pdf(paper_filename, jpg_dir):
    doc = fitz.open()
    imgs = []
    img_path = './{}/'.format(jpg_dir)
    if len(os.listdir('./{}/'.format(jpg_dir)))<100:
        print("文章{}下载错误，跳过".format(paper_filename))
        return
    for img in os.listdir('./{}/'.format(jpg_dir)):
        imgs.append(img)
    imgs.sort(key=lambda x:int(x[:-4]))
    #print(imgs)
    for img in imgs:
        #print(img_path + img)
        img_file = img_path + img
        imgdoc = fitz.open(img_file)
        pdfbytes = imgdoc.convertToPDF()
        pdf_name = str(img[:-4]) + '.pdf'
        imgpdf = fitz.open(pdf_name, pdfbytes)
        doc.insertPDF(imgpdf)
    filename = './papers/' + paper_filename
    doc.save(filename)
    doc.close()

if __name__=='__main__':
    main()