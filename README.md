# MyTieBa
获取单个贴吧帖子详细数据的程序。

##功能实现

+ 已实现功能：


1. 获取某个贴吧前N页帖子列表，列表信息包括：帖子URL，标题，回帖数，回帖页数，发帖日期，发帖时间；
2. 将帖子列表保存到同目录下的tiebadb中；
3. 获取帖子的回复列表，列表信息包括：回帖楼层，回帖内容，回帖字数，回帖ID，回帖时间，回帖链接；


+ 即将实现功能:


1. 手动输入贴吧名；
2. 某个时间段内的所有帖子列表；
3. 统计某个ID在该贴吧内的发帖数据；
4. 统计一段时间内优质帖。



##运行方式

**该程序运行需本机安装有MySQL且已手动建立数据库tiebadb及数据表tiezilist。**

###数据库准备

+ 进入数据库环境：

`mysql -u root -p;`

+ 创建tiebadb数据库：

`create database tiebadb character set utf8;`

+ 选择tiebadb数据库：

`use tiebadb;`

+ 创建tiezilist数据表并定义列：

`create table tiezilist(url varchar(300),topic varchar(300),revertnm int(10),pagenm int(10),pgdate date,pgtime time;`

此处定义了六个列，分别用于存放帖子URL，标题，回复数，回复页数，发帖日期，发帖时间。

+ 建立程序使用的用户并赋予权限：

`create user pub@localhost identified by 'password';`

`grant all on tiebadb.* to 'pub'@'localhost';`

### 运行

直接运行程序：

`python MyTieBa.py`

输入需要抓取的页数（0~50之间的数字），程序即可自动获取帖子列表并写入tiebadb的tiezilist表中。

###查询结果

查询表中所有值：

`select * from tiezilist`

按回帖页数的倒序显示帖子标题，回帖数，回帖页数列：

`select distinct topic,revertnm,pagenm from tiezilist order by pagenm desc;`