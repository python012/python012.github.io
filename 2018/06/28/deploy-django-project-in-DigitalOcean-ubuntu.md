---
title: "在DigitalOcean云服务器上部署Django项目实践笔记"
date: 2018-06-28
tags:
  - Python
  - Django
description: "首先得有一份Django app项目代码，在本地调试模式下(python manage.py runserver)跑起来各种没问题。 配置云服务器在DigitalOcean上申请Ubuntu 16.04LTS的Droplet，拿到公网IP和root密码，登陆后安装Django项目中用到的数据库软件，比如MySql: 12345sudo apt-get updatesudo apt-get -y u"
---

# 在DigitalOcean云服务器上部署Django项目实践笔记

<div class="article-meta">
  <span class="date">📅 发布于：2018年06月28日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Python</span> <span class="tag">Django</span></span>
</div>

首先得有一份Django app项目代码，在本地调试模式下(`python manage.py runserver`)跑起来各种没问题。

## 配置云服务器

在DigitalOcean上申请Ubuntu 16.04LTS的Droplet，拿到公网IP和root密码，登陆后安装Django项目中用到的数据库软件，比如MySql:

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install mysql-server
sudo apt isntall mysql-client
sudo apt install libmysqlclient-dev

```bash

执行命令`sudo netstat -tap | grep mysql`来检查MySql是否在运行，登录打开MySql提示符执行`mysql> create database proj_db_name character set utf8;`来预创建Django项目要用到的数据库，这里数据库名字为proj_db_name。

执行`sudo apt-get -y install nginx`安装NGINX，用来服务支持静态文件(css,js, images)，还可以在代理服务器下运行Django app。

安装Supervisor，用来启动和管理Django应用程序服务。

```bash
sudo apt-get -y install supervisor
sudo systemctl enable supervisor
sudo systemctl start supervisor

```bash

安装Python 3.x，我实践中是安装的3.6版本，那就需要去下载Python 3.6源码做编译安装。

执行`sudo apt-get -y install python-virtualenv`安装Python Virtualenv，使用virtualenv已然是Python项目的最佳实践之一，它可以方便的建立独立python依赖空间，避免项目之间可能的依赖冲突问题。一般实践中是`virtualenv venv`在项目根目录下生成保存独立python环境与依赖的venv目录。

添加项目专用的用户，执行`adduser joe`，这里joe就是用户名，然后`gpasswd -a joe sudo`加入到sudo用户列表。

执行`su - joe`切换到joe账号，当前目录应该是`/home/joe`，再执行`virtualenv -p python3 .`，也即在当前目录生成一份独立python环境，python版本和系统命令python3指向的python版本一致，如果不加`-p python3`则就和默认命令python指向的python版本一致，再继续执行`source bin/activate`启用这个独立虚拟python环境。

```text
joe@ubuntu-s-1vcpu-1gb-sfo2:~$sourcebin/activate
(joe) joe@ubuntu-s-1vcpu-1gb-sfo2:~$ ls
bin  include  lib  logs  pip-selfcheck.json  run
(joe) joe@ubuntu-s-1vcpu-1gb-sfo2:~$

```bash

## 设置Django项目

git clone项目代码到`/home/joe`，执行`git clone https://github.com/python012/guest.git`，继续执行`pip install -r guest/requirements.txt`安装所有依赖。

注意这里guest是Django项目(as Django app)名字。

修改Django项目中的`./guest/guest/settings.py`，以下是修改后的一个diff：

```properties
-DEBUG = True
+DEBUG = False# 在生产环境中必须关闭DEBUG模式

-ALLOWED_HOSTS = []
+ALLOWED_HOSTS = ['167.99.104.197',]# 云主机的公网IP

# Application definition
@@ -81,11 +81,11 @@ DATABASES = {
'ENGINE':'django.db.backends.mysql',
-'HOST':'---------',
+'HOST':'127.0.0.1',
'PORT':'3306',
-'NAME':'guest',
+'NAME':'proj_db_name',
'USER':'MySqlUsername',
-'PASSWORD':'---------',
+'PASSWORD':'MysqlPassword',
'OPTIONS': {
'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
},
@@ -132,9 +132,10 @@ USE_TZ = False

STATIC_URL ='/static/'

+STATIC_ROOT ='/home/joe/www/static'# 静态文件目录

```bash

回到当前目录`/home/joe`，生成静态文件目录`mkdir /home/joe/www/static`，执行`python manage.py migrate`连接MySql初始化各个数据表，再执行`python manage.py createsuperuser`来生成管理员账户，最后执行`python manage.py collectstatic`。

## 设置Gunicorn、Supervisor、NGINX

执行`pip install gunicorn`安装Gunicorn(可能是发音G unicorn)，这是一个WSGI容器(WSGI HTTP Server)。

执行`vim bin/gunicorn_start`，文件内容如下：

```bash
#!/bin/bash

NAME="guest"
DIR=/home/joe/guest
USER=joe
GROUP=joe
WORKERS=3
BIND=unix:/home/joe/run/gunicorn.sock
DJANGO_SETTINGS_MODULE=guest.settings
DJANGO_WSGI_MODULE=guest.wsgi
LOG_LEVEL=error

cd$DIR
source../bin/activate

exportDJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
exportPYTHONPATH=$DIR:$PYTHONPATH

exec../bin/gunicorn${DJANGO_WSGI_MODULE}:application \
--name$NAME\
--workers$WORKERS\
--user=$USER\
--group=$GROUP\
--bind=$BIND\
--log-level=$LOG_LEVEL\
--log-file=-

```bash

执行`chmod u+x bin/gunicorn_start`，给gunicorn_start文件添加执行权限。在用户目录`/home/joe`下生成run、logs两个目录。执行`touch logs/gunicorn-error.log`用来保存Django app错误日志。

执行`sudo vim /etc/supervisor/conf.d/guest.conf`生成一个Supervisor配置文件，文件内容如下：

```properties
[program:guest]
command=/home/joe/bin/gunicorn_start
user=joe
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/joe/logs/gunicorn-error.log

```text

刷新Supervisor的配置文件信息，启动Django app。

```bash
sudo supervisorctl reread
sudo supervisorctl update

```bash

继续设置Nginx，执行`sudo vim /etc/nginx/sites-available/guest`生成Django app对应的配置文件，文件内容如下：

```text
upstream app_server {
server unix:/home/joe/run/gunicorn.sock fail_timeout=0;
}

server {
# 如果设置为80则可以外网用户可以通过直接访问云主机的公网IP来打开Django app
listen 8089;

# add here the ip address of your server
# or a domain pointing to that ip (like example.com or www.example.com)
server_name 167.99.104.197;

keepalive_timeout 5;
client_max_body_size 4G;

access_log /home/joe/logs/nginx-access.log;
error_log /home/joe/logs/nginx-error.log;

location /static/ {
alias /home/joe/www/static/;
}

# checks for static file, if not found proxy to app
location / {
try_files $uri @proxy_to_app;
}

location @proxy_to_app {
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $http_host;
proxy_redirect off;
proxy_pass http://app_server;
}
}

```

执行`sudo ln -s /etc/nginx/sites-available/guest /etc/nginx/sites-enabled/guest`创建符号链接，执行`sudo rm /etc/nginx/sites-enabled/default`删除NGINX默认的网站配置，最后执行`sudo service nginx restart`来重启nginx，这时候应该能够通过云服务器的公网IP访问Django app了，注意还需要加上配置的端口号8089，如果设置为80则可直接访问IP了。如果后期Django项目代码有更改，可以执行`sudo supervisorctl restart guest`来重启Djang app以应用最新项目代码。