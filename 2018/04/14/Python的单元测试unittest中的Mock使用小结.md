---
title: "Python的单元测试unittest中的Mock使用小结"
date: 2018-04-14
tags:
  - python
  - unittest
description: "Part One前面一篇博文简单说了使用unittest.mock对无返回值的函数做单元测试，这里是更多一些例子的总结。 被测函数中使用到了input需要自动化输入12345678910111213141516171819#!/usr/bin/env python3from unittest import TestCasefrom unittest.mock import patchfrom un"
---

# Python的单元测试unittest中的Mock使用小结

<div class="article-meta">
  <span class="date">📅 发布于：2018年04月14日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span> <span class="tag">unittest</span></span>
</div>

# Part One

前面一篇博文简单说了使用`unittest.mock`对无返回值的函数做单元测试，这里是更多一些例子的总结。

## 被测函数中使用到了input需要自动化输入

```python
#!/usr/bin/env python3

fromunittestimportTestCase
fromunittest.mockimportpatch
fromunittestimportmain

deffunc_input():
name = input("Enter your name: ")
print('Your name is {}'.format(name))

def test_func_input():
  with patch('builtins.input') as mocked_input:
    mocked_input.side_effect = ('Jo',) #当input的时候会输入Jo
  with patch('builtins.print') as mocked_print:
    func_input()
    mocked_print.assert_called_with('Your name is Jo')

if__name__ =='__main__':
  main()
```

## 需要验证函数是否被“被测函数“调用

```python
#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch
from unittest import main

deffunc_1():
func_2()

deffunc_2():
print("It's func 2!")

def test_func_1():
  with patch('func_2') as mocked_func_2:
    func_1()
    mocked_func_2.assert_called_once() #断言mocked_func_2被调用过一次，在执行func_1()后

if__name__ =='__main__':
  main()
```

## mock.patch()和mock.patch.object()的区别

这一块我还不是特别明白，搜索了下，大致区别如下

> 

mock.patch() doesn’t require that you import the object before patching, while mock.patch.object() does require that you import before patching

有一个遗留问题，如下代码中，完全不能使用mock.patch()吗？

```python
# py_unittest.py

from unittest import TestCase
from unittest.mockimport patch
from unittest import main

classPerson(object):

  def __init__(self, name):
    self.name = name

  def print_name(self):
    print('My name is '+ self.name)

  def print_parents(self):
    mother = input("Enter mother's name: ")
    father = input("Enter father's name: ")

    print("{}'s parents are {} and {}.".format(self.name, mother, father))
    self.fake_func()

  def fake_func(self):
    pass

classFuncTest(TestCase):
def test_print_parents(self):
  john = Person('John')

with patch('builtins.input') as mocked_input:
  mocked_input.side_effect = ('Jo','Lee')
  withpatch('builtins.print') as mocked_print:
  withpatch.object(Person,"fake_func") as mocked_fake_func:
  # with patch('Person.fake_func') as mocked_fake_func: 启用这里的话，会报
  # 错 ModuleNotFoundError: No module named 'Person'

john.print_parents()
mocked_print.assert_called_with("John's parents are Jo and Lee.")
mocked_fake_func.assert_called_once()

if__name__ =='__main__':
  main()
```

# Part Two

今天研究了下，问题解决了，关键还是一个查找module的问题。

## 小结一个import的基础用法

很多源代码里看到这样的用法，`from flask import Flask`，`from models.item import ItemModel`，然后当我自己创建了一个名字叫person的module的时候，如果我也想在其他代码里方便的使用`from person import Person`来导入`Person`类的话，可以这样做。

创建person目录，同时目录下有`__init__.py`和`person.py`两个文件，

![](/images/20180416203026947.png)

`person.py`中定义了一个`Person`类，有`__init__.py`文件存在，则会定义这个目录是一个module，同时文件内容如下：

```python
__all__ = ['Person',]

from.person import Person

```

这样在其他module或者python代码里，就可以通过`from person import Person`来导入`Person`类了，假如`__init__.py`是空的，则需要使用`from person.person import Person`来导入`Person`类。

回到最开始mock.patch()的问题，解决代码可见于segmentfault上问题[关于mock.patch()和mock.patch.object()的区别的问题]的回答。