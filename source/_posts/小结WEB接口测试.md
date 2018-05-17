---
title: 小结WEB接口测试
date: 2018-03-16 22:20:12
tags: [接口测试, Python]
---

最近在做一个接口测试的更新，往里面添加了很多新的测试，连续加班两周，这里做一些总结。

## 被测设备介绍

这是一个针对某款智能设备的WEB API的测试，设备内运行OpenWRT系统，内部使用一套节点来记录很多设备信息和配置信息，设备也提供一个WEB GUI页面，可以通过打开其主页来做配置，也提供了一套WEB 接口API，来实现远程设置功能（其实就是给WEB GUI页面来调用）

## 测试框架介绍

测试用python实现，主要用到的有单元测试框架pytest，HTTP库requests，还有ssh连接用的pamamiko。

## 工作背景

这次工作之前，这套接口测试已经基本成型，运行了一段时间，最近是根据客户要求，往其中添加更多的set测试。可以理解为，已经有的测试多数是get测试，使用类似于cgi?get=wifi_status这样的query去获WEB的response，也即一个json串，再继续解析出设备上Wi-Fi的具体信息的值，再针对这些值做一些验证（和通过ssh登陆上设备调用shell命令获取的信息进行对比）。

## 总结与反思

  - 设计测试后的时候，有些是简单的举一反三和想当然，因此浪费了一些时间。测试中获取的信息有这样几个途径：一是向设备发送get请求，会收到带json串的response，json串中即是返回的信息，这一点是API文档中认可的。二是向设备发送set请求（确实是发送GET请求而不是POST，设计如此，也即发送GET请求，该请求中包含类似于&act=set&service=wifi&enabled=0这样的信息），也会收到带json串的response，也可以解析出返回的信息。然后我最开始错误的认为，这里json串的信息是可以用来验证结果，实际上这一点是API文档中并没有提到的，这里完全是我想当然，没有事先验证我的想法的结果就是，白白浪费了一些时间，走了弯路。
  - 加set测试的时候，我基本是一气code完，事后证明，还是应该做完一个后，想办法在本地跑起来，和熟悉这部分的同事做一个简单的评审，确保我的理解是和大家一致的，然后再继续做其他的部分。
  - 格式良好、易读的log打印会帮助迅速定位失败的测试，了解到测试执行的时候到底发生了什么事情。这点太重要了，这套接口测试其实也由我维护的（分析失败的测试，报bug或者更新测试代码），以前我就加了一个log打印，比如这个函数Util.printQueryAndJson()，望文生义，就是当发送一个request请求后，执行这个函数，把刚刚发送的request请求里的query字符串，和返回的response的json串打印出来。这里我就犯了个错误，以为set请求返回的json串是可以和get请求后返回的json一样，可以拿来做验证，实际上却不是。

下面是重构测试代码的时候，用到的一段python代码，用到函数里的内部函数特性，也称为闭包：

``` python
#!/usr/bin/env python

def run():
        a = {"name":"Li Ming", "age":23}

        def inner_func():
                a.clear()#此处python自动识别出这是一个外部变量a
                a.update({"language":"python"})
        inner_func()
        print(a)


        def new_inner_func():
                a = {"language":"java"} #此处未能影响外部的变量a，只是一个内部函数里变量

        new_inner_func()
        print(a)

run()
```

执行结果是

``` bash
{'language': 'python'}
{'language': 'python'}
```