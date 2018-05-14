---
title: 不使用IDE的情况下，导入自定义Python module的最佳实践
date: 2018-05-04 21:38:19
tags: [python]
---

# Part 1

微软出的Visual Studio Code这个代码编辑器很好用，和Sublime有点相似，但是用起来更方便一些。和PyCharm不一样，用VS code写自定义module的时候，会出现找不到module的报错，原因是VS code不会像IDE那样，帮用户把项目目录临时性加入到系统PATH中去。

今天做了些探索，目前可行的方法大致如下，但是仍然不能算是最佳实践，已经在CPyUG上提了这个问题，看看有没有什么更好的办法。

``` python
#!/usr/bin/env python3

import os
import sys

base_path = os.path.dirname(os.path.abspath(__file__)) + '\\..\\'

sys.path.append(base_path) #这里临时性的把项目目录加入到系统路径中

from utils.config_reader import ConfigReader #这样才可以导入位置在 ../utils/config_reader.py 里的 ConfigReader 类
print(ConfigReader)
```
# Part 2

CPyUG确实是个挺好的组织，Python方面的问题一般都会有热心又专业的小伙伴帮忙回答，针对上次导入自定义Python module的问题，目前有两个可行的办法。

方法1是针对应用了pytest框架的测试项目的，例如有如下项目结构。

<pre>
  TEST_PROJECT
     /testlogin
        test_login.py
     /util
        __init__.py
        global_values.py
    conftest.py
<code>

项目中定义了一个包`util`，其中有模块`global_values.py`，在另一个目录`testlogin`中有`test_login.py`希望导入模块`global_values.py`，这里就需要在项目根目录下创建一个`conftest.py`文件（内容为空也是允许的），这样，当在项目根目录下执行pytest来启动测试的时候，pytest会帮你识别整个项目目录中的各种自定义模块，不会出现找不到模块的问题。

``` python
import pytest
from util import global_values #导入自定义模块

def test_login():
    print(global_values.USER_NAME)
    assert 5 == 5
```
通过这个解答，我发现pytest里对conftest.py的应用还挺有意思的，[stackoverflow里这篇解答](https://stackoverflow.com/questions/34466027/in-py-test-what-is-the-use-of-conftest-py-files)写的很棒，值得一看！

另一个方法是通过配置一个系统变量PYTHONPATH，python在查找module的时候会这个变量定义的目录里去查找，所以在不同平台下临时性定义这个系统变量，也是个解决导入自定义模块的办法。我猜想PyCharm就是用了这个方法来让用户方便导入模块的吧。