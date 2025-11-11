---
title: "实现Selenium Webdriver自动化测试中对失败测试进行截图并发布到Jenkins"
date: 2018-01-23
tags:
  - Jenkins
  - Java
  - Selenium
  - Junit4
description: "在基于Selenium Webdriver(Java) + Junit4 + Jenkins 的web 自动化测试中，进行失败test的截图，同时发布到Jenkins上。 这两天在研究这个问题，这是一点总结，首先需要版本够高的Jenkins，并安装Junit Attachments plugin，同时注意要去Jenkins配置Additional test report features，选择启用"
---

# 实现Selenium Webdriver自动化测试中对失败测试进行截图并发布到Jenkins

<div class="article-meta">
  <span class="date">📅 发布于：2018年01月23日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Jenkins</span> <span class="tag">Java</span> <span class="tag">Selenium</span> <span class="tag">Junit4</span></span>
</div>

在基于Selenium Webdriver(Java) + Junit4 + Jenkins 的web 自动化测试中，进行失败test的截图，同时发布到Jenkins上。

这两天在研究这个问题，这是一点总结，首先需要版本够高的Jenkins，并安装[Junit Attachments plugin]，同时注意要去Jenkins配置Additional test report features，选择启用 Publish test attachments，这样这个Junit Attachments插件可以帮助检查标准输出中，是否有特定格式的关于附件的log，然后依据log中的附件文件的地址，把该附件上传至Jenkins中。

还需要代码里的支持，我手上的web自动化测试，是基于Selenium Webdriver(Java) + Junit4实现的，这里需要实现一个Junit4里的 rule，我这是ScreenshotRule，继承于TestWatcher，改写其中的failed()方法，也即当 test case failed 的时候，执行截图操作，具体代码如下：

```java
packagecom.ibm.robot.web.testrules;

importjava.io.File;
importjava.io.IOException;
importorg.apache.commons.io.FileUtils;

importorg.junit.rules.TestWatcher;
importorg.junit.runner.Description;

importorg.openqa.selenium.OutputType;
importorg.openqa.selenium.TakesScreenshot;
importorg.openqa.selenium.WebDriver;

publicclassScreenshotRuleextendsTestWatcher{

privateWebDriver driver =null;
publicScreenshotRule(WebDriver driver){
this.driver = driver;
}

@Override
protectedvoidfailed(finalThrowable e,finalDescription description){

String userDir = System.getProperty("user.dir");
String baseDir = userDir +"/failed-screenshots/"
+ description.getClassName() +"/";
String screenshotName = description.getClassName() +"."
+ description.getMethodName() +".png";

File screen =null;
screen = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);

try{
File dir =newFile(baseDir);
if(!dir.exists()) FileUtils.forceMkdir(dir);
File localFile =newFile(baseDir + screenshotName);
FileUtils.copyFile(screen, localFile);

// Work with JUnit Attachments plugin to attach the files
// produced by Junit to Jenkins
System.out.println("[[ATTACHMENT|"+ baseDir + screenshotName +"]]");
}catch(IOException ioe) {
ioe.printStackTrace();
}
}
}

```text

最后还要去test的基类中，启用这个rule，注意这个rule类在使用的时候，需要传入test的基类中使用的driver，也即：

```text
@Rule
publicScreenshotRule screenshotRule =newScreenshotRule(driver);

```