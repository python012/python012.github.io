---
title: '''Master Jenkins CI For DevOps and Developers''课程总结'
date: 2018-04-04 00:07:47
tags: [Jenkins, DevOps, CI]
---

这个课程的内容不算多，不到一个星期就看完了，赶紧来做个总结和笔记。

课程中的内容大致分为3部分。

 - 普通的Jenkins pipeline的创建。从github（git）上pull代码，触发的时间设置（Poll SCM），配置JDK、Maven、Git，配置Maven项目，Maven项目中clean package后收集生成的war包，job之间的触发的互相依赖，使用pipeline插件，让pipeline更加的可视化。
 - Jenkins pipeline as code的实现，就是把pipeline的建立、各项具体配置都写在jenkinsfile里。在创建job的时候，选择pipeline而不是freestyle。
 - Jenkins master和slave结构的建立。

## Jenkins master和slave结构的建立

重点记一下这部分。

课程中的目标是，使用两台ubuntu主机，一台作为master，一台作为slave。为了方便起见，这里是申请了https://www.digitalocean.com/ 里的两台ubuntu 16.04LTS主机。

先登陆master主机上安装Jenkins，具体命令

 1. `wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -`
 2. `echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list`
 3. `apt-get update`
 4. `apt-get install jenkins`

参考链接[https://jenkins.io/doc/book/installing/#debian-ubuntu](https://jenkins.io/doc/book/installing/#debian-ubuntu)，注意默认会去安装Jenkins的最新版，安装指定版本可用`apt-get install jenkins=2.67`。

实际验证中发现Ubuntu主机上没有安装JDK，所以还要先安装jdk8。命令如下

 1. `sudo add-apt-repository ppa:webupd8team/java`
 2. `sudo apt update`
 3. `sudo apt install oracle-java8-installer`

参考链接是http://tipsonubuntu.com/2016/07/31/install-oracle-java-8-9-ubuntu-16-04-linux-mint-18/

还可以继续安装jre，命令是`sudo apt install oracle-java8-set-default`。

另外在master的Ubuntu上安装Maven后，还需要去Global Tool Configuration里去配置JDK，Git和Maven的路径，下面是我配置的默认路径：

![](/images/20180429212000957.png)

然后需要master主机上生成一对rsa密钥，再在master和slave上执行以下命令，达到可以无密码访问slave主机效果

> sudo -iu jenkins
> ssh root@slave_ip mkdir -p .ssh
> cat .ssh/id_rsa.pub | ssh root@slave_ip 'cat >> .ssh/authorized_keys'

在slave主机上执行

> mkdir ~/bin
> cd bin
> wget http://master_ip:8080/jnlpJars/slave.jar

打开运行master主机上的Jenkins主页，登陆后新建一个node，Remote root directory可填`/var/jenkins`，Launch command填`ssh root@slave_ip java -jar /root/bin/slave.jar`，保存后刷新页面，slave node应该就连接上了。后面就应该就简单了，可以继续配置slave node的lable，然后配置job在具体某个lable上执行。

第一部分普通jenkins pipeline的建立，还需要再复习一下。

完成课程后可以拿个证书。
![](/images/UC-TG6ZI0V3.png)