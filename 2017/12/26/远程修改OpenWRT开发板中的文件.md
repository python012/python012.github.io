---
title: "远程修改OpenWRT开发板中的文件"
date: 2017-12-26
tags:
  - Python
  - 接口测试
  - Shell
  - Linux
description: "这两天收到一个任务，某接口测试的测试用例需要更新，需要在测试中修改开发板中的文件。 先白话下上层的一些东西，包括这套接口测试在内，可见的全部测试都挂在Jenkins上，测试对象是某刷了OpenWRT修改版的智能设备，Jenkins上游自然是自动编译生成build文件的各种job（有主线和针对不同需求的分支），一旦成功生成新的build文件，就会触发下游各种各样的测试，其中包括接口测试。 挂在Jen"
---

# 远程修改OpenWRT开发板中的文件

<div class="article-meta">
  <span class="date">📅 发布于：2017年12月26日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Python</span> <span class="tag">接口测试</span> <span class="tag">Shell</span> <span class="tag">Linux</span></span>
</div>

这两天收到一个任务，某接口测试的测试用例需要更新，需要在测试中修改开发板中的文件。

先白话下上层的一些东西，包括这套接口测试在内，可见的全部测试都挂在Jenkins上，测试对象是某刷了OpenWRT修改版的智能设备，Jenkins上游自然是自动编译生成build文件的各种job（有主线和针对不同需求的分支），一旦成功生成新的build文件，就会触发下游各种各样的测试，其中包括接口测试。

挂在Jenkins上的所有测试大都基于一个公司内部用shell实现的基础测试框架，包含了很多基本函数，像刷build，ssh连接执行命令，试探主机是否在线，获取主机版本号等等，然后到了具体测试的实现的时候，就各显神通了，大部分测试都由shell实现，web页面测试的有Selenium Webdriver和Casperjs。

废话完了说重点，要解决的问题就是要远程登录到OpenWRT开发板（智能硬件）上修改某文件( /etc/config/fw )，要找到该文件后在文件中某行下添加一行语句，比如找到 /etc/config/fw 文件，在文件找到 config firewall 这一行，再在这一行下插入一条 option blacklist ‘1’。

测试中是在基础测试框架中的 control.sh 里执行 python3 -m py.test –junitxml=./result/results.xml 来把测试拉起来，于是就查找python里做远程ssh登录执行Linux的方法，找到paramiko模块，最后实现代码大致以下，sed那一段挺麻烦，不过总算是找到解决方法了。

```python
defsshclient_execmd(cmd):
try:
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(hostname=list.host_ip, port=22, username=list.username, password=list.password,timeout=5)
stdin, stdout, stderr = s.exec_command(command=cmd,timeout=30)
returns,stdout
exceptExceptionase:
print(e)
s.close()
returns,None

sshclient_execmd('''sed -i '/^config.*firewall/a\        option blacklist '"'1'"'' /etc/config/fw''')

```