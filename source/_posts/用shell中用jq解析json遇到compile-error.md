---
title: 用shell中用jq解析json遇到compile error
date: 2017-12-05 23:18:12
tags: [Shell, Json]
---

前几天接到任务，需要完善一段shell写的测试脚本，其中的问题最后归结成这样一个问题，已知如下json格式的字符串：

``` json
{  
    "up": true,
    "pending": false,  
    "available": true,  
    "autostart": true,  
    "dynamic": false,  
    "uptime": 5217,  
    "ipv4-address": [  
        {  
            "address": "192.168.59.150",  
            "mask": 24  
        }  
    ],  
    "ipv6-address": [  
          
    ],  
    "ipv6-prefix": [  
          
    ],  
    "ipv6-prefix-assignment": [  
          
    ],  
    "route": [  
          
    ]  
}  
```

目标是需要解析获得ipv4-address.address的值，网上搜了下，一般shell命令行里推荐使用jq，试用后发现一个有意思的问题，仿佛jq不太喜欢field name中间有dash，也就是那一小段横线，执行`cat data.json > jq -r '.ipv4-address.address'` 就会报compile error。

进一步搜索，用bing的国际版终于找到相关页面，见[https://github.com/stedolan/jq/issues/38](https://github.com/stedolan/jq/issues/38)，也即这是jq的bug。可用的解决方案最终如下：

``` bash
cat data.json > jq -r '.["ipv4-address"][0].address'
```