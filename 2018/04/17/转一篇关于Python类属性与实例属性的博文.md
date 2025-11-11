---
title: "转一篇关于Python类属性与实例属性的博文"
date: 2018-04-17
tags:
  - python
description: "链接见 https://segmentfault.com/a/1190000002671941 小结下我的理解，如下一个Person类 12345678910class Person(object):    school_name = \"ABC school\"    def __init__(self, name):        self.name = name        def print"
---

# 转一篇关于Python类属性与实例属性的博文

<div class="article-meta">
  <span class="date">📅 发布于：2018年04月17日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span></span>
</div>

链接见[https://segmentfault.com/a/1190000002671941]

小结下我的理解，如下一个Person类

```python
classPerson(object):
school_name ="ABC school"

def__init__(self, name):
self.name = name

defprint_name(self):
print('My name is '+ self.name)

jo = Person('Jo')

```

其中的`school_name`就是一个类属性，它可以通过`Person.school_name`和`jo.school_name`（在jo已经通过`Person('Jo')`实例化为一个`Person`对象后）来访问到。

实际上，在jo刚刚实例化为一个`Person`对象后，jo是没有`school_name`属性的，此时如果有`print(jo.school_name)`这样的操作，实际上也是去访问的`Person`这个类对象的`school_name`属性。除非主动给`jo.school_name`赋值，不然jo一直不会有自己的`school_name`属性。

在jo拥有自己的`school_name`属性之后，对`jo.school_name`的修改操作，不会去改变`Person.school_name`的值，因为如上所说，`Person`类本身也是一个拥有`school_name`属性的对象，它的属性`school_name`只能通过`Person.school_name`来修改。

感谢原作者！[_zhao]