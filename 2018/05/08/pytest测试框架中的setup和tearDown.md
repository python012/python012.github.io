---
title: "pytest测试框架中的setup和tearDown"
date: 2018-05-08
tags:
  - python
  - pytest
description: "Part One最近对pytest比较感兴趣，看了pytest的文档classic xunit-style setup，这里做个小结，直接看代码。 123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676"
---

# pytest测试框架中的setup和tearDown

<div class="article-meta">
  <span class="date">📅 发布于：2018年05月08日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span> <span class="tag">pytest</span></span>
</div>

# Part One

最近对pytest比较感兴趣，看了pytest的文档[classic xunit-style setup]，这里做个小结，直接看代码。

```bash
# content of test_websites.py

'''
Setup/teardown in pytest, see https://docs.pytest.org/en/3.5.1/xunit_setup.html

Remarks:
1. setup/teardown的结对函数在测试进程中可以被调用多次的。
2. 如果setup函数在执行时失败或被skipped了，相应的tearDown函数不会被调用。
'''

importpytest

defsetup_module(module):
"""
这是一个module级别的setup，它会在本module(test_website.py)里
所有test执行之前，被调用一次。
注意，它是直接定义为一个module里的函数"""
print()
print("-------------- setup before module --------------")

defteardown_module(module):
"""
这是一个module级别的teardown，它会在本module(test_website.py)里
所有test执行完成之后，被调用一次。
注意，它是直接定义为一个module里的函数"""
print("-------------- teardown after module --------------")

classTestBaidu(object):

deftest_login(self):
print("test baidu login function")
assertTrue==True

classTestSohu(object):

@classmethod
defsetup_class(cls):
""" 这是一个class级别的setup函数，它会在这个测试类TestSohu里
所有test执行之前，被调用一次.
注意它是一个@classmethod
"""
print("------ setup before class TestSohu ------")

@classmethod
defteardown_class(cls):
""" 这是一个class级别的teardown函数，它会在这个测试
类TestSohu里所有test执行完之后，被调用一次.
注意它是一个@classmethod
"""
print("------ teardown after class TestSohu ------")

defsetup_method(self, method):
""" 这是一个method级别的setup函数，它会在这个测试
类TestSohu里，每一个test执行之前，被调用一次.
"""
print("--- setup before each method ---")

defteardown_method(self, method):
""" 这是一个method级别的teardown函数，它会在这个测试
类TestSohu里，每一个test执行之后，被调用一次.
"""
print("--- teardown after each method ---")

deftest_login(self):
print("sohu login")
assertTrue==True

deftest_logout(self):
print("sohu logout")
pytest.skip()

```python

pytest中的setup/teardown还有一个更推荐的实现方法是去使用pytest.fixture特性，上面这种经典的setup/teardown，pytest表示也会继续支持。下面准备总结下用pytest.fixture实现setup/teardown的方法。

# Part Two

下面内容是阅读文档[pytest fixtures: explicit, modular, scalable]的一些总结，pytest fixture功能很丰富，功能远不止用来构建测试中传统的setup/teardown。

但是还是先看下用pytest.fixture特性写的setup/teardown，据[stakoverflow上一哥们]说，这还是目前的最佳实践。

```python
importtime
importpytest
fromseleniumimportwebdriver
fromselenium.webdriver.common.byimportBy
fromutils.logimportlogger
fromutils.configimportget_url

@pytest.fixture()
defchrome_driver(scope="function"):
"""
scope="function"是scope的默认值，表示这是一个function级别的fixture
"""
print("setup() begin")
driver = webdriver.Chrome()
driver.get(get_url())
print("setup() end")
yielddriver
#这里会返回driver，给使用这个fixture为参数的test_函数使用，
#test_函数结束后，会回到这里，继续执行后面语句
print("teardown() begin")
driver.close()
print("teardown() end")

classTestBaiDu(object):

locator_kw = (By.ID,'kw')
locator_su = (By.ID,'su')
locator_result = (By.XPATH,'//div[contains(@class, "result")]/h3/a')

deftest_search_0(self, chrome_driver):
"""
这里的chrome_driver是在本模块中定义的fixture，这里输入
的参数是上面yield driver中返回的driver
"""
chrome_driver.find_element(*self.locator_kw).send_keys(u'selenium 测试')
chrome_driver.find_element(*self.locator_su).click()
time.sleep(2)
links = chrome_driver.find_elements(*self.locator_result)
forlinkinlinks:
logger.info(link.text)

```text

这样写看起来有点pythonic的味道，我理解写这样fixture形式的setup/teardown函数，主要还是给那些需要打开然后关闭的资源，比如上面例子中的浏览器driver，确实需要收尾（`driver.quit()`）。

可能还有其他应用，比如写一个数据库查询的函数，就可以把连接数据库，获得数据查询句柄，yield 句柄，关闭数据库句柄，关闭数据连接写成一个fixture，这样代码应该清爽多了。

```python
@pytest.fixture(scope="module") #一个module里的所有函数共用一个句柄实例
defsql_query():
#连接数据库
#获得数据库查询句柄
yield"查询句柄"
#关闭句柄
#关闭数据库连接

```text

fixture如果不用到yield，则只是把fixture函数里返回的值，作为参数给到使用fixture的函数，代码如下

```python
@pytest.fixture()
deffruit_name():
return"apple"

deftest_fruit(fruit_name):
assert"apple"== fruit_name

```