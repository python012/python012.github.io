---
title: 用Shell精简log文件(shell的字符串和文件操作)
date: 2016-11-29 16:31:15
tags: [Shell,]
---

当前目录下有文件log，内容大致如下

``` text
2015-11-29 54144a04ad4asd044a4s CSeq:1 INVITE sip:2112@sipserver.com:5060 SIP/2.0
2015-11-29 54144a04ad4asd045457 CSeq:1 INVITE SIP/2.0 200 OK
```

将此log文件做精简，创建文件minilog内容如下

``` text
1 INVITE sip:2112@sipserver.com:5060 SIP/2.0
1 INVITE SIP/2.0 200 OK
```

Shell脚本代码如下

``` bash
#!/bin/sh

function shortLog() {
  while read line
    do
      echo ${line#*CSeq:} >> $2
  done < $1
}

shortLog log miniLog
```