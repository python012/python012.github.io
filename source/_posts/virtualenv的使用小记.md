---
title: virtualenv的使用小记
date: 2018-04-17 20:48:50
tags: [python, virtualenv]
---

virtualenv可以用来创建一套虚拟的、独立的、干净python环境，如果系统中安装有多个python版本，则还可以指定版本。

`pip install virtualenv`  pip安装virtualenv。
`virtualenv venv --python=python3.6` 创建一个名字叫venv的python环境，python版本指定为3.6，然后virtualenv会在当前目录下创建名为venv的目录。
`virtualenv --no-site-packages venv` 创建一个名字叫venv的，无第三方包的干净的python环境，python版本与系统中的版本一致。
`source venv/bin/activate` 启用venv环境。
`pip install -r requirements.txt` 安装文件requirements.txt里列举的第三方python模块，也即是当前的venv环境中安装。

在PyCharm中使用virtualenv作为项目解释器（Project Interpreter）时，选择Add Local -> Exisiting environment，Interpreter再定位到venv/bin/python并选中即可。

`deactivate` 关闭venv环境。
