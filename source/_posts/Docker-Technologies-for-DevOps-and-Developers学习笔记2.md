---
title: Docker Technologies for DevOps and Developers学习笔记 - 2
date: 2018-05-20 17:28:10
tags: [docker]
---
# Build custom docker image

## 使用docker commit命令来创建docker image

**General steps**:
  - Spin up a container from a base image.
  - Install Git package in the container.
  - Commit changes made in the container.

把Docker国内镜像`https://registry.docker-cn.com`添加至docker `registry-mirrors`。

或者可直接用命令拉取镜像，例如`docker pull registry.docker-cn.com/library/ubuntu:16.04`

国内镜像配置好后，执行`docker run -it debian:jessie`，拉取debian镜像并进入container。

在debian container后，执行`apt-get update && apt-get install -y git`，在container中安装Git。

安装完成后执行`exit`退出，再执行`docker images -a`查找刚刚安装了git的debian container的ID。

执行`docker commit GIT_DEBIAN_CONTAINER_ID reed/debian:1.00`来新建一个安装了Git的debian docker image，完成后可使用`docker images`来查看本地image列表。

完成以上后，就可以在本地执行`docker run -it reed/debian:1.00` 来**新建一个debian container并进入**，可以发现**container中已经安装好了Git**。

## 使用Dockerfile来创建docker image

以debian:jessie为base image，新建一个安装了Git和vim的image，以下是Dockerfile。

```
FROM debian:jessie
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y vim
```

然后执行`docker build -t reed/gitvim/debian .`，表示在当前目录下搜索Dockerfile，新image的REPOSITORY名字为reed/gitvim/debian。

但是，实践中可能会遇到因为网络等问题引起的安装不顺利，感觉还是直接用commit命令来手动创建custom image比较合适。

**Good Practice** -> Dockerfile也可这样写：

```
FROM debian:jessie
RUN apt-get update && apt-get install -y \
  git \
  vim
```

-> 避免重复的package同时让列表易于更新：

```
FROM debian:jessie
RUN apt-get update && apt-get install -y \
  git \
  python \
  vim
```
-> 另一个例子，CMD中的命令仅当container运行的时候执行

```
FROM debian:jessie
RUN apt-get update && apt-get install -y \
  git \
  python \
  vim
CMD ["echo", "hello docker"]
```

-> 为保证apt-get update是最新的，运行Dockerfile的时候可以关闭docker cache -> `docker build -t reed/debian . --no-cache=true`

-> CMD中加入copy命令，复制文件到container中去，下面Dockerfile生成的container将会从当前目录中复制文件

```
FROM debian:jessie
RUN apt-get update && apt-get install -y \
  git \
  python \
  vim
COPY abc.txt /src/abc.txt
```

-> CMD中还有ADD命令，ADD可以理解是升级版的COPY，可以从网上下载文件，也可以自动化解压缩文件，通常优先使用COPY，除非非常肯定没问题的情况下则使用ADD。