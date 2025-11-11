---
title: "重构一份应用pytest框架的测试代码"
date: 2018-05-13
tags:
  - python
  - pytest
  - 重构
description: "项目中有份API测试的代码的结构大致如下  /api_test    – test_device_api01_via_lan.py    – test_device_api02_via_lan.py    – test_device_api03_via_lan.py    – test_device_api01_via_wan.py    – test_device_api02_via_wan.p"
---

# 重构一份应用pytest框架的测试代码

<div class="article-meta">
  <span class="date">📅 发布于：2018年05月13日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span> <span class="tag">pytest</span> <span class="tag">重构</span></span>
</div>

项目中有份API测试的代码的结构大致如下

> 

/api_test
– test_device_api01_via_lan.py
– test_device_api02_via_lan.py
– test_device_api03_via_lan.py
– test_device_api01_via_wan.py
– test_device_api02_via_wan.py
– test_device_api03_via_wan.py

很容易猜到其实这里是重复的2份代码，只是因为执行测试的时候，有一份是通过lan测试，另一份是通过wan测试。每次修改代码，还需要把修改同步到相应的lan或者wan的代码上去……

但是又不能简单的做个循环，把lan/wan的地址丢进去当参数，因为项目目前运行是需要收集JUnit格式的测试报告的，优化代码后，还需要拿到和之前一样或者差不多的报告，好显示在Jenkins上。

今天实在不能忍了，花点时间研究了下，有如下解决办法。

项目根目录上新建一个conftest.py，内容如下

```properties
defpytest_generate_tests(metafunc):
idlist = []
argvalues = []
forscenarioinmetafunc.cls.scenarios:
idlist.append(scenario[0])
items = scenario[1].items()
argnames = [x[0]forxinitems]
argvalues.append(([x[1]forxinitems]))
metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

scenario1 = ('LAN', {'URL':'www.baidu.com'})
scenario2 = ('WAN', {'URL':'www.sohu.com'})

```text

tests目录下任一个test模块，大致做如下修改

```properties
importpytest
fromconftestimportscenario1, scenario2

classTestLogin(object):
scenarios = [scenario1, scenario2]

deftest_login_01(self, URL):
assert"www"inURL

deftest_login_02(self, URL):
assert"ok"=="ok"

deftest_login_03(self, URL):
assert"sohu"inURL

```text

然后执行以上测试的时候，虽然代码里只写了3个测试，实际上pytest会生成以下6个测试，生成的JUnit测试报告也会有这6个测试的测试结果。

```bash
rx:pytest_proj reed$ pytest --collect-only tests/test_api01.py
=============testsession starts ======
platform darwin -- Python 3.6.5, pytest-3.5.1, py-1.5.3, pluggy-0.6.0
rootdir: /Users/reed/Documents/dev/pytest_proj, inifile:
collected 6 items
<Module'tests/test_api01.py'>
<Class'TestLogin'>
<Instance'()'>
<Function'test_login_01[LAN]'>
<Function'test_login_02[LAN]'>
<Function'test_login_03[LAN]'>
<Function'test_login_01[WAN]'>
<Function'test_login_02[WAN]'>
<Function'test_login_03[WAN]'>

```