---
title: 在云服务器上使用Python+Selenium+Jenkins搭建webUI测试 - 0
date: 2018-05-29 17:41:34
tags: [Selenium, Python, Xvfb, Jenkins]
---

在[www.digitalocean.com](www.digitalocean.com)上租了个Ubuntu 16.04的云服务器，用优惠码可以新用户送15刀，大约是最小配置的服务器可以用3个月，而且是按分钟算钱，除了网速有时候可能慢点，实在是没有其他缺点了。

有云服务器后，还需要安装以下一些软件：

- Firefox, 普通的`sudo apt-get install firefox`会安装最新版本的Firefox，正确的做法是去[Mozilla的服务器](https://ftp.mozilla.org/pub/firefox/releases/)上找指定的版本，然后用wget下载到服务器里去，我这次是用的版本46的安装包，`wget https://ftp.mozilla.org/pub/firefox/releases/46.0/linux-x86_64/en-US/firefox-46.0.tar.bz2`，再`tar -jxvf firefox-46.0.tar.bz2`解压缩，得到一个firefox目录，可以放到`/lib`目录中，再生成一个link文件`ln -s /lib/firefox/firefox /usr/bin/firefox`，最后在任意目录下执行`firefox -version`正常输出版本的话就ok了。
- Xvfb, `sudo apt-get install xvfb`，解决没有主机没有屏幕可能会导致的无法连接Firefox的异常。
- geckodriver, Firefox浏览器的webdriver驱动，需要去[Github-geckodriver-releases](https://github.com/mozilla/geckodriver/releases)，比如下载0.19.0版本的geckodriver，wget到主机上后，添加执行权限，再mv到`/usr/bin`目录。
- Jenkins, JDK。
- Jenkins安装[Xvfb Plugin](https://wiki.jenkins.io/display/JENKINS/Xvfb+Plugin)，还需要去Jenkins的全局工具设置中配置Xvfb的安装目录，在webUI job里需要配置启动Xvfb。
- `pip install`安装Python3、pytest、selenium等依赖。

搭建过程中遇到最耗时间的还是geckodriver和Firefox版本匹配的问题，最开始安装的最新的60的Firefox和最新版本的geckodriver，几次尝试后发现应该是geckodriver支持不了这么高版本的Firefox，然后对Firefox进行降级，最后geckodriver 0.19.0和Firefox 46.0适配成功。

至此，环境配置部分基本完成了，如果Selenium代码ok的话应该是可以正常运行，后续打算继续给套测试添砖加瓦，完善test case基类，页面对象等工作。
