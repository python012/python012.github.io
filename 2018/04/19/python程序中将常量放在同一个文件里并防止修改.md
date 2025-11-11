---
title: "python程序中将常量放在同一个文件里并防止修改"
date: 2018-04-19
tags:
  - python
description: "在看《编写高质量代码-改善Python程序的91个建议》一书，是国内Python圈和CPyUG里的名人赖总和人合著的，里面建议了很多比较好，比较Pythonic的代码写法，打算边看边实践，挑选一些记录下，这算是第一篇吧。 常量也就是那些一般不会变的数据，建议的做法如下： 1234567891011121314151617181920212223242526'''Best practice 01Pu"
---

# python程序中将常量放在同一个文件里并防止修改

<div class="article-meta">
  <span class="date">📅 发布于：2018年04月19日</span>
  <span class="tags">🏷️ 标签：<span class="tag">python</span></span>
</div>

在看《编写高质量代码-改善Python程序的91个建议》一书，是国内Python圈和CPyUG里的名人赖总和人合著的，里面建议了很多比较好，比较Pythonic的代码写法，打算边看边实践，挑选一些记录下，这算是第一篇吧。

常量也就是那些一般不会变的数据，建议的做法如下：

```python
'''
Best practice 01

Put all constants in one file, and protect them from changing value.

'''
# File name: constants.py

classConst(object):
classConstError(TypeError):
pass

classConstCaseError(ConstError):
pass

def__setattr__(self, name, value):
ifnameinself.__dict__:# 判断是否已经被赋值，如果是则报错
raiseself.ConstError("Can't change const.%s"% name)
ifnotname.isupper():# 判断所赋值是否是全部大写，用来做第一次赋值的格式判断，也可以根据需要改成其他判断条件
raiseself.ConstCaseError('const name "%s" is not all supercase'% name)

self.__dict__[name] = value

const = Const()
const.MY_CONSTANT ="CHINA"
const.MY_SECOND_CONSTANT ="RUSSIA"

```

```bash
#File name: test.py
fromconstantsimportconst
print(const.MY_CONSTANT)
const.MY_CONSTANT =2#此处尝试再赋值会触发ConstError

```