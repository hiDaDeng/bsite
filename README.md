# 一、简介

bsite是用于采集B站用户视频列表页、视频评论数据的python包。





# 二、安装

```
pip install bsite
```



# 三、使用方法

## 3.1 初始化Bsite类

需要先登录B站，使用开发者工具获取自己浏览器上的的cookies。获取方法可以参考 [京东评论实战视频](https://www.bilibili.com/video/BV1AE411r7ph?p=6 )  



```python
from bsite import Bsite

cookies = {"cookie": "登录B站后的cookies"}
bs = Bsite(cookies=cookies)
```

<br><br>

## 3.2 bvid与aid转换

B站的视频链接 

```
https://www.bilibili.com/video/BV1AE411r7ph
```

其中 **BV1AE411r7ph** 是该视频的 **bvid号**， 但在B站后台有一个与bvid对应的id号- **aid**

bvid与aid可以互相转化，Bsite内置了两个转化方法

- **Bsite.aid2bvid(aid)**
- **Bsite.bvid2aid(bvid)**



例如将BV1AE411r7ph转为aid

```python
bs.bvid2aid(bvid="BV1AE411r7ph")
```

```
72010301
```



同理将 72010301 转为 bvid

```python
bs.aid2bvid(aid=72010301)
```

```
BV1AE411r7ph
```

<br><br>

## 3.3 下载某用户所有视频信息



**Bsite.video_list(mid, csvfpath)** 获取用户的所有已上传的视频信息。

- mid 用户的id，例如我的B站视频主页https://space.bilibili.com/122592901  其中122592901就是mid
- csvfpath csv文件路径，用于存储视频信息。

> 注意：为了保证所有数据均能正常存储不出错，强制使用utf-8编码，微软office打开该csv会乱码，可以用记事本或者WPS打开



一般在B站查看某用户【投稿】栏，可以看到ta的所有上传视频。Bsite可以帮我们得到的信息有

- title、subtitle、author 标题、副标题、作者
- aid、bvid 视频链接的id号
- mid 用户的id。例如我的B站视频主页https://space.bilibili.com/122592901  其中122592901就是mid
- created 上传时间
- description 视频简介
- pic 视频首图
- play 播放次数
- length 视频时长

获取**DJI大疆创新** https://space.bilibili.com/232472043/video 所有投稿视频相关信息。

```python
bs.video_list(mid=232472043, csvfpath='dji_videos.csv')
```



## 3.4 获取某视频内的所有评论

**Bsite.comments(aid, csvfpath)**

- aid  B站视频的id号，如果只有bvid没有aid，可以先使用内置的方法把bvid转为aid

- csvfpath csv文件路径，用于存储评论数据。

    

> 注意：为了保证所有数据均能正常存储不出错，强制使用utf-8编码，微软office打开该csv会乱码，可以用记事本或者WPS打开

采集到的评论数据包括

- content  评论内容
- device 评论者使用的设备
- like 点赞数
- rcount 该评论追评和互动数
- ctime 评论创建时间
- avatar 评论者头像
- level 评论者等级
- sex 评论者性别
- sign 评论者签名
- uname 评论者昵称
- mid 评论者的id
- diag 该评论是原始评论，还是某评论的互动



获取该视频 https://www.bilibili.com/video/BV1E54y1C7MF 所有的评论

```python
aid = bs.bvid2aid('BV1E54y1C7MF')
bs.comments(aid=aid, csvfpath='comments.csv')
```





## 如果

如果您是经管人文社科专业背景，编程小白，面临海量文本数据采集和处理分析艰巨任务，个人建议学习[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)视频课。作为文科生，一样也是从两眼一抹黑开始，这门课程是用五年时间凝缩出来的。自认为讲的很通俗易懂o(*￣︶￣*)o，

- python入门
- 网络爬虫
- 数据读取
- 文本分析入门
- 机器学习与文本分析
- 文本分析在经管研究中的应用

感兴趣的童鞋不妨 戳一下[《python网络爬虫与文本数据分析》](https://ke.qq.com/course/482241?tuin=163164df)进来看看~



## 更多

- [B站:大邓和他的python](https://space.bilibili.com/122592901/channel/detail?cid=66008)

- 公众号：大邓和他的python

- [知乎专栏：数据科学家](https://zhuanlan.zhihu.com/dadeng)

    ​    

## 支持一下

![](img/my_zanshang_qrcode.jpg)