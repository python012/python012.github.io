---
title: '''Docker Technologies for DevOps and Developers''学习笔记'
date: 2018-05-19 22:04:59
tags: [Docker]
---

## Concepts

Images
  - which are read only templates used to create containers.
  - are created with the docker build command by docker user.

Containers
  - container is an instance of an image(like an instance of a class - a runtime object)

Official Docker images website -> [https://hub.docker.com/](https://hub.docker.com/)

## Basic commands

ls本机上的docker image -> `docker images`

创建一个有busybox的的docker container 并执行 `echo "hello docker"` -> `docker run busybox:1.24 echo "hello docker"`

ls docker container中的根目录 -> `docker run busybox:1.24 ls /`

进入docker container -> `docker run -i -t busybox:1.24`，执行`exit`可退出container，每一次都是一个新的image

使用`docker ps -a`来查看创建过的历史container ->

``` bash
rx:dev reed$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                 CREATED             STATUS                         PORTS               NAMES
d46a47c46f34        busybox:1.24        "sleep 1000"            3 minutes ago       Up 3 minutes                                       wonderful_shockley
180a27bc3ba4        busybox:1.24        "sh"                    4 minutes ago       Exited (0) 4 minutes ago                           nostalgic_ritchie
901dec3242bb        busybox:1.24        "ls /"                  26 minutes ago      Exited (0) 26 minutes ago                          pensive_keldysh
```
新建一个container执行命令，完成后自动删除这个container -> `docker run --rm busybox:1.24 sleep 1`

新建一个指定名字的docker container -> `run --name my_docker_container busybox:1.24 ls`

inspect一个container的底层信息 ->

``` bash
rx:dev reed$ docker run -d busybox:1.24 sleep 100
7dd3d07d1ae16e0ccd042c62cc08a2523dc3dbf325ea9f957ff49fcf1e414645
rx:dev reed$ docker inspect 7dd3d07d1ae16e0ccd042c62cc08a2523dc3dbf325ea9f957ff49fcf1e414645
```

拉取tomcat 8.0 image，并创建一个container，同时将container的8080端口映射到主机的8888端口 ->

  - 从国内docker image源中下载tomcat 8.0 image -> `docker pull registry.docker-cn.com/library/tomcat:8.0`
  - 创建container并映射端口 -> `docker run -it -p 8888:8080 registry.docker-cn.com/library/tomcat:8.0`
  - 运行container并在后台运行 -> `docker run -it -d -p 8888:8080 registry.docker-cn.com/library/tomcat:8.0` 执行后会显示container ID
  - 查看后台运行的container的运行log -> `docker logs DOCKER_CONTAINER_ID`
  - 停止一个后台运行的container -> `docker stop DOCKER_CONTAINER_NAME`

## Run Container in Foreground or Background

run container in foreground -> default mode

run container in background -> `-d`(dispatch) option

建一个container在后台运行，并用`ps`查看运行中的container ->

``` bash
rx:dev reed$ docker run -d busybox:1.24 sleep 1000
d46a47c46f34cbec69dc6ce04e9674a74f81d5bea17b93a8d441c4a88c8ba056
rx:dev reed$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
d46a47c46f34        busybox:1.24        "sleep 1000"        1 second ago        Up 2 seconds                            wonderful_shockley
```
