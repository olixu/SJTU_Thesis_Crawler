# -*- coding:utf-8 -*-

import requests
import json
import shutil
import os
import time
import sys
from lxml import etree
from bs4 import BeautifulSoup
from collections import defaultdict
import fitz
import time
import argparse
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', type=str, required=True)
    args = parser.parse_args()
    pages = args.pages.split('-')
    #print(pages[0])
    #print(pages[1])
    info_url = "http://thesis.lib.sjtu.edu.cn/sub.asp?content=%E8%87%AA%E5%8A%A8%E5%8C%96&choose_key=department&xuewei=1&px=2&page="
    #info_url = "http://thesis.lib.sjtu.edu.cn/sub.asp?content=%E8%AE%A1%E7%AE%97%E6%9C%BA&choose_key=department&xuewei=1&px=2&page="
    pages = [int(pages[0]), int(pages[1])]
    papers = download_main_info(info_url, pages)
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
        #print(info_url_construction)
        #print(50*'&')
        response = result.get(info_url_construction, headers=headers, allow_redirects=False)
        #with open('test.html', 'wb') as f:
        #    f.write(response.content)

        html = etree.HTML(response.content, etree.HTMLParser())

        for i in range(2, 22):
            #print(i)
            # 有些是论文保密，所以link需要错误处理
            info_dict = defaultdict(str)
            try:
                filename = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]//td[2]/text()'.format(i))[0]
                author = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[3]/div/text()'.format(i))[0]
                mentor = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[6]/div/text()'.format(i))[0]
                year = html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[8]/div/text()'.format(i))[0]
                link = "http://thesis.lib.sjtu.edu.cn/" + html.xpath('/html/body/section/div/div[3]/div[2]/table/tr[{}]/td[9]/div/a[2]/@href'.format(i))[0]
                #print(filename)
                #print(author)
                #print(mentor)
                #print(year)
                #print(link)
                #print(50*'#')
                info_dict['filename'] = filename
                info_dict['author'] = author
                info_dict['mentor'] = mentor
                info_dict['year'] = year
                info_dict['link'] = link
                papers.append(info_dict)
            except:
                pass
   # print(papers)
    print("总共抓取到{}个元数据信息".format(len(papers)))
 

    #soup = BeautifulSoup(response.text.encode('utf-8'), 'html.parser')
    #table = soup.find('table')
    #print(table)


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