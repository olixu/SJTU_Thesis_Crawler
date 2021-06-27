# 上海交通大学-学位论文系统下载器

## 问题：
[http://thesis.lib.sjtu.edu.cn/](http://thesis.lib.sjtu.edu.cn/)，该网站是上海交通大学的学位论文下载系统，收录了交大的硕士博士的论文，但是，该版权保护系统用起来很不方便，加载起来非常慢，所以该下载器实现将网页上的每一页的图片合并成一个PDF。

## 解决方案：
使用`PyMuPDF`对图片进行合并

## 安装依赖：
```bash
pip install -r requirements.py
```

## 使用方式：
```bash
python downloader.py
```

## ToDo List
1. 如何解决`thesis.lib.sjtu.edu.cn`限制访问次数的问题
2. 引入协程，提高并发（以前试过，不过由于网站太慢了，并行就崩了），多进程的版本可以看[commit](https://github.com/olixu/SJTU_Thesis_Crawler/tree/7d712f009195f339d1cc42e6bf841db57f881052)
3. 改进交互能力及已存在的bug

