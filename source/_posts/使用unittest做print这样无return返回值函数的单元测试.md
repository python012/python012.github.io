---
title: 使用unittest做print这样无return返回值函数的单元测试
date: 2018-04-11 21:40:29
tags: [python, unittest]
---

在看Python里自带的一个单元测试库unittest，有个有意思的应用是可以对类似于print()这样无return返回值的函数做验证。见下面代码。

``` python
#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch
from unittest import main

class Person(object):
    def __init__(self, name):
        self.name = name
    
    def print_name(self):
        print('My name is ' + self.name)

class FuncTest(TestCase):
    def test_print_name01(self):
        john = Person('John')

        with patch('builtins.print') as mocked_print:
            john.print_name()
            mocked_print.assert_called_with('My name is John')

    def test_print_name02(self):
        john = Person('Donald')

        with patch('builtins.print') as mocked_print:
            john.print_name()
            mocked_print.assert_called_with('My name is Donald')

if __name__ == '__main__':
    main()

```
执行结果

``` bash
reedx:garrulous_py_practice reed$ python3 py_unittest_01.py
..
------------------------------------
Ran 2 tests in 0.001s
 
OK
```

其中的```with patch('builtins.print') as mocked_print:``` 语句是在with的block里，将内置函数print替换为mocked_print函数，再去block里执行print，实际也就是在执行mocked_print函数，然后去检查mocked_print函数是否收到同样的传入参数，也即检查了print语句的输出（print语句自然是传入什么样的字符串，就输出打印出什么样的字符串）。

显而易见，这就是去验证目标函数或者方法的传入参数，单元测试里可以应用的范围很广。