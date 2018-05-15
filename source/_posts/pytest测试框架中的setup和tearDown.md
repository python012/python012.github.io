---
title: pytest测试框架中的setup和tearDown
date: 2018-05-08 21:51:19
tags: [pytest, python]
---

# Part One

最近对pytest比较感兴趣，看了pytest的文档[classic xunit-style setup](https://docs.pytest.org/en/3.5.1/xunit_setup.html#classic-xunit-style-setup)，这里做个小结，直接看代码。

``` python
# content of test_websites.py

'''
Setup/teardown in pytest, see https://docs.pytest.org/en/3.5.1/xunit_setup.html

Remarks:
1. setup/teardown的结对函数在测试进程中可以被调用多次的。
2. 如果setup函数在执行时失败或被skipped了，相应的tearDown函数不会被调用。
'''

import pytest

def setup_module(module):
    """
    这是一个module级别的setup，它会在本module(test_website.py)里
    所有test执行之前，被调用一次。
    注意，它是直接定义为一个module里的函数"""
    print()
    print("-------------- setup before module --------------")


def teardown_module(module):
    """
    这是一个module级别的teardown，它会在本module(test_website.py)里
    所有test执行完成之后，被调用一次。
    注意，它是直接定义为一个module里的函数"""
    print("-------------- teardown after module --------------")


class TestBaidu(object):

    def test_login(self):
        print("test baidu login function")
        assert True == True


class TestSohu(object):

    @classmethod
    def setup_class(cls):
        """ 这是一个class级别的setup函数，它会在这个测试类TestSohu里
        所有test执行之前，被调用一次.
        注意它是一个@classmethod
        """
        print("------ setup before class TestSohu ------")

    @classmethod
    def teardown_class(cls):
         """ 这是一个class级别的teardown函数，它会在这个测试
         类TestSohu里所有test执行完之后，被调用一次.
        注意它是一个@classmethod
        """
        print("------ teardown after class TestSohu ------")

    def setup_method(self, method):
        """ 这是一个method级别的setup函数，它会在这个测试
         类TestSohu里，每一个test执行之前，被调用一次.
        """
        print("--- setup before each method ---")
    
    def teardown_method(self, method):
        """ 这是一个method级别的teardown函数，它会在这个测试
         类TestSohu里，每一个test执行之后，被调用一次.
        """
        print("--- teardown after each method ---")

    def test_login(self):
        print("sohu login")
        assert True == True

    def test_logout(self):
        print("sohu logout")
        pytest.skip()

```

pytest中的setup/teardown还有一个更推荐的实现方法是去使用pytest.fixture特性，上面这种经典的setup/teardown，pytest表示也会继续支持。下面准备总结下用pytest.fixture实现setup/teardown的方法。

# Part Two

下面内容是阅读文档[pytest fixtures: explicit, modular, scalable](https://docs.pytest.org/en/latest/fixture.html)的一些总结，pytest fixture功能很丰富，功能远不止用来构建测试中传统的setup/teardown。

但是还是先看下用pytest.fixture特性写的setup/teardown，据[stakoverflow上一哥们](https://stackoverflow.com/a/39401087/2526362)说，这还是目前的最佳实践。

``` python
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.log import logger
from utils.config import get_url

@pytest.fixture()
def chrome_driver(scope="function"):
    """
    scope="function"是scope的默认值，表示这是一个function级别的fixture
    """
    print("setup() begin")
    driver = webdriver.Chrome()
    driver.get(get_url())
    print("setup() end")
    yield driver 
    #这里会返回driver，给使用这个fixture为参数的test_函数使用，
    #test_函数结束后，会回到这里，继续执行后面语句
    print("teardown() begin")
    driver.close()
    print("teardown() end")


class TestBaiDu(object):

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def test_search_0(self, chrome_driver):
        """
        这里的chrome_driver是在本模块中定义的fixture，这里输入
        的参数是上面yield driver中返回的driver
        """
        chrome_driver.find_element(*self.locator_kw).send_keys(u'selenium 测试')
        chrome_driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = chrome_driver.find_elements(*self.locator_result)
        for link in links:
            logger.info(link.text)
```

这样写看起来有点pythonic的味道，我理解写这样fixture形式的setup/teardown函数，主要还是给那些需要打开然后关闭的资源，比如上面例子中的浏览器driver，确实需要收尾（`driver.quit()`）。

可能还有其他应用，比如写一个数据库查询的函数，就可以把连接数据库，获得数据查询句柄，yield 句柄，关闭数据库句柄，关闭数据连接写成一个fixture，这样代码应该清爽多了。

``` python
@pytest.fixture(scope="module") #一个module里的所有函数共用一个句柄实例
def sql_query():
    #连接数据库
    #获得数据库查询句柄
    yield "查询句柄"
    #关闭句柄
    #关闭数据库连接
```

fixture如果不用到yield，则只是把fixture函数里返回的值，作为参数给到使用fixture的函数，代码如下

``` python
@pytest.fixture()
def fruit_name():
    return  "apple"

def test_fruit(fruit_name):
    assert "apple" == fruit_name

```

