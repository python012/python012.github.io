---
title: CI/CD在Jenkins上的简易实现
date: 2018-04-05 21:42:19
tags: [Jenkins, CI]
---


## Build job

在pipeline的最上游的Build job里的Configure里做如下设置，可使该job以1分钟1次的频率，去轮询Git repository里的代码，如果有更新，则即刻开始build。`* * * * *`表示轮询频率是每一天的每一分钟，这里是用的Cron表达式，具体可见[Cron Format](http://www.nncron.ru/help/EN/working/cron-format.htm)。

![](/images/20180405214711474.png)

Continous Delivery（持续交付），里面当然包含了自动化部署，以Java实现的web app项目为例，部署就需要拿到编译通过并打包好的war包文件，并部署到Tomcat服务器上。

在job Configure -> Build -> **Invoke top-level Maven targets**里填入 ```clean package```，然后在Post-build Actions里添加**Archive the artifacts**，填入```**/*.war```，表示寻找所有war文件并存档到workspace里。

当然Build job里也是可以跑单元测试和做静态代码检查的。

继续在Configure -> Post-build Actions里添加**Build other projects**，在这里填入下游的staging job的名字。

## Staging job

在用来部署staging环境的job里，需要用到[Copy Artifact](https://plugins.jenkins.io/copyartifact)插件，和[Deploy to container](https://plugins.jenkins.io/deploy)插件。

Configure->Build里添加**Copy artifacts from another project**，Artifact to copy里填```**/*.war```，Post-build Actions里添加**Deploy war/ear to a container**，Container里选择合适的容器，比如Tomcat 8.x，设置好Credentials和Tomcat URL，保存。顺利的话，至此，启动上游Build job成功后，会拉起这个staging job，会把war包部署到Tomcat里，这时候打开Tomcat下的web app的链接，就能看到运行的web app了，这也意味着可以开始下一步的产品测试，比如接口测试和Selenium实现的Web UI测试。

最后使用[Build Pipeline Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin)插件，新建pipeline view，可获得下面的可视化的pipeline效果。

![](/images/20180407001336964.png)




