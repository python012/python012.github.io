---
title: 在Maven+Jenkins项目里添加Java静态代码质量检查并发布报告
date: 2018-04-05 18:11:08
tags: [Maven, Jenkins]
---


需要的插件：

 - [Maven Integration plugin](https://wiki.jenkins.io/display/JENKINS/Maven+Project+Plugin)
 - [Checkstyle Plug-in](https://wiki.jenkins.io/display/JENKINS/Checkstyle+Plugin)

具体步骤：

 1. 新建job，选择Freestyle project。 Source Code Management选择Git，填入Repository URL。
 2. Build中添加Invoke top-level Maven targets，Maven Version里选择之前在Manage Jenkins->Gloabl Tool Configuration里设置的Maven name.
 3. Goals里填入Maven命令，比如clean package，这里为了添加Java静态代码检查功能，实际设置为```clean package checkstyle:checkstyle```。
 4. Post build actions里添加Publish Checkstyle analysis results，再Save。
 5. 下次build即可见到代码质量报告，和非常具体的错误提示。

效果如图

![](/images/20180405202722385.png)

![](/images/20180405202740728.png)


----------

 可选的其他静态代码检查工具插件：
 - [PMD Jenkins plugin](https://wiki.jenkins-ci.org/display/JENKINS/PMD+Plugin)
 - [Findbugs Jenkins Plugin](https://wiki.jenkins-ci.org/display/JENKINS/FindBugs+Plugin)

 



