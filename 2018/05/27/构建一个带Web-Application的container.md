---
title: "构建一个有Web Application的container"
date: 2018-05-27
tags:
  - docker
description: "课程中的例子中是用Flask框架的web app，大致步骤如下。 首先把代码clone下来，执行git clone git@github.com:jleetutorial/dockerapp.git 有Dockerfile如下： 1234567FROM python:3.5RUN pip install Flask==1.0.2RUN useradd -ms /bin/bash adminUSER"
---

# 构建一个有Web Application的container

<div class="article-meta">
  <span class="date">📅 发布于：2018年05月27日</span>
  <span class="tags">🏷️ 标签：<span class="tag">docker</span></span>
</div>

课程中的例子中是用Flask框架的web app，大致步骤如下。

首先把代码clone下来，执行`git clone git@github.com:jleetutorial/dockerapp.git`

有Dockerfile如下：

```dockerfile
FROM python:3.5
RUN pip install Flask==1.0.2
RUN useradd -ms /bin/bash admin
USER admin
WORKDIR /app
COPY app /app
CMD ["python", "app.py"]

```text

有`app\app.py`，一个Flask的web app如下：

```properties
fromflaskimportFlask
app = Flask(__name__)

@app.route('/')
defhello_world():
return'Hello, World!'

if__name__ =='__main__':
app.run(host='0.0.0.0')

```text

在`app.py`的上层目录执行`docker build -t dockerapp:v0.1 .`，构建一个docker image.

执行`docker images`来查询本机上所有的docker image，可以发现dockerapp已经在列表中了。

```text
rx:dockerapp reed$ docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED              SIZE
dockerapp                               v0.1                1661743950e7        About a minute ago   700MB

```text

运行一个dockerapp的container，`-d`表示在后台运行，`-p`表示端口映射，执行结果返回container ID。

```text
rx:app reed$ docker run -d -p 5000:5000 1661743950e7
2312dc563731677c5b127628df2312889bd8d9b3104560d56154a0c0498f13c0

```text

然后可以用`docker ps`来查询运行中的container列表。

```bash
rx:app reed$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
2312dc563731        1661743950e7"python app.py"2 minutes ago       Up 2 minutes        0.0.0.0:5000->5000/tcp   dreamy_torvalds

```text

打开本机浏览器访问`http://localhost:5000/`，即可看到web app已经在运行，并显示`Hello, World!`。

进入后台中运行的container(interactive模式)并执行一些命令

```text
rx:app reed$ dockerexec-it 2312dc563731 bash
admin@f5f0334b04a0:/app$pwd
/app
admin@f5f0334b04a0:/app$cd/home/admin/
admin@f5f0334b04a0:~$ ps axu
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
admin        1  0.0  1.2 252100 25340 ?        Ss   11:49   0:00 python app.py
admin        9  0.1  0.1  21956  3676 pts/0    Ss   11:54   0:00 bash
admin       16  0.0  0.1  19188  2380 pts/0    R+   11:54   0:00 ps axu

```

学到这里感觉docker应用很广啊，至少在配置自动化测试环境上应该很好使。