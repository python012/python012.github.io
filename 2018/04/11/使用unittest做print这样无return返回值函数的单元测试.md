---
title: "使用unittest做print这样无return返回值函数的单元测试"
date: 2018-04-11
tags:
  - python
  - unittest
description: "在看Python里自带的一个单元测试库unittest，有个有意思的应用是可以对类似于print()这样无return返回值的函数做验证。见下面代码。 123456789101112131415161718192021222324252627282930#!/usr/bin/env python3from unittest import TestCasefrom unittest.mock imp"
---

# 使用unittest做print这样无return返回值函数的单元测试

<div class="article-meta">
  <span class="date">📅 发布于：2018年04月11日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span> <span class="tag">unittest</span></span>
</div>

在看Python里自带的一个单元测试库unittest，有个有意思的应用是可以对类似于print()这样无return返回值的函数做验证。见下面代码。

```bash
#!/usr/bin/env python3

fromunittestimportTestCase
fromunittest.mockimportpatch
fromunittestimportmain

classPerson(object):
def__init__(self, name):
self.name = name

defprint_name(self):
print('My name is '+ self.name)

classFuncTest(TestCase):
deftest_print_name01(self):
john = Person('John')

withpatch('builtins.print')asmocked_print:
john.print_name()
mocked_print.assert_called_with('My name is John')

deftest_print_name02(self):
john = Person('Donald')

withpatch('builtins.print')asmocked_print:
john.print_name()
mocked_print.assert_called_with('My name is Donald')

if__name__ =='__main__':
main()

```text

执行结果

```text
reedx:garrulous_py_practice reed$ python3 py_unittest_01.py
..
------------------------------------
Ran 2 testsin0.001s

OK

```

其中的`with patch('builtins.print') as mocked_print:`语句是在with的block里，将内置函数print替换为mocked_print函数，再去block里执行print，实际也就是在执行mocked_print函数，然后去检查mocked_print函数是否收到同样的传入参数，也即检查了print语句的输出（print语句自然是传入什么样的字符串，就输出打印出什么样的字符串）。

显而易见，这就是去验证目标函数或者方法的传入参数，单元测试里可以应用的范围很广。