# 可以运行JS脚本工具

## 环境配置
1. 在安装环境时，需要进行安装casperjs
```
其它版本的详细信息可以见[官网](http://casperjs.org/)
先去安装PhantomJS然后在安装casperjs

sudo apt-get install phantomjs
$ git clone git://github.com/casperjs/casperjs.git
$ cd casperjs
$ ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs
$ phantomjs --version
$ casperjs --version
```

2. 运行run.sh脚本时，程序会自动下载制定的页面下载到html中
```
sh run.sh
$ ls html 
1.html   14.html  17.html  20.html  25.html  3.html
```

3. 运行extractUserID.py脚本，可以将html中的网页提取出来制定的用户名
```
```