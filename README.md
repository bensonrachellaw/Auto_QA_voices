# Auto_QA_voices
Python 3.6-flag: making a voice dialogue question answering robot system (WEB version)

首先，本项目分为制作语音机器人后台部分和利用flask搭建网页部分。
博客地址：https://blog.csdn.net/bensonrachel/article/details/107794695

制作语音机器人：

本系统的功能有：与图灵机器人进行对话；设置闹钟（计时器）；播放本地音乐：机器写古诗；

1.与图灵机器人对话的部分，参考了[这篇博客](https://blog.csdn.net/NIeson2012/article/details/96476878#01-%E5%88%9D%E5%BF%83%E7%BC%98%E7%94%B1)

2.闹钟功能，这里使用了多线程的技术，把用户语音设定的时间转为文字且交给另一个线程去执行时间流逝，到点即响应报时。

3.播放音乐，需要使用的包为pygame，而且暂时只能播放本地音乐。

4.机器人写古诗的功能，我用训练好的模型生成古诗，再录入图灵机器人的问答库里即可。

网页部分

flask项目的目录结构是这样的，

这次一共设置了两个页面，分别是my-link.html,template.html;

这是简单的flask初使用。可视为参考博客的一个网页版应用，再加了一两个小功能。