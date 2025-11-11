---
title: "Jenkins执行完构建后testng插件找不到testng-results.xml"
date: 2018-03-23
tags:
  - Jenkins
  - TesgNG
description: "昨天把Jenkins(ver. 2.107.1，此处注意，这几乎是一个最新的Jenkins版本)安装在mac上，并建了一个简单的job，来体验下Jenkins+Maven+TestNG的效果，遇到这样一个有意思的问题，就是使用默认设置，也配置了TestNG的测试结果报告插件。  当Jenkins构建执行后，也可以正常找到指定的pom.xml文件，并执行Maven命令mvn test -PmyTes"
---

# Jenkins执行完构建后testng插件找不到testng-results.xml

<div class="article-meta">
  <span class="date">📅 发布于：2018年03月23日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Jenkins</span> <span class="tag">TesgNG</span></span>
</div>

昨天把Jenkins(ver. 2.107.1，此处注意，这几乎是一个最新的Jenkins版本)安装在mac上，并建了一个简单的job，来体验下Jenkins+Maven+TestNG的效果，遇到这样一个有意思的问题，就是使用默认设置，也配置了TestNG的测试结果报告插件。

![](/images/20180323203141603.png)

当Jenkins构建执行后，也可以正常找到指定的pom.xml文件，并执行Maven命令mvn test -PmyTestngProfile.xml来启动测试，但是测试完成后，却显示：

```text
TestNG Reports Processing: START
Looking for TestNG results report in workspace using pattern: **/target/surefire-reports/testng-results.xml
Did not find any matching files.

```

花了点时间研究下，在Configure里的TestNG XML report pattern里，只有设置为完全绝对路径的时候，才能找到testng-results.xml。

揭晓答案吧，其实就是当构建进行到去寻找testng-results.xml的时候，当前目录并不是最开始的项目代码目录（pom.xml所在的目录），而是下面这个Jenkins在mac上安装后的一个默认workspace，然后以此为当前目录继续构建工作。

> 

/Users/Shared/Jenkins/Home/workspace/myProject

解决办法是去构建的Configure -> General -> Advanced… -> Use custom workspace，也即使用自定义的工作空间目录，把这个目录设置为项目代码的真实地址，然后构建就会以此为当前目录，然后就可以顺利找到testng的报告文件了。

![](/images/20180323202739548.png)