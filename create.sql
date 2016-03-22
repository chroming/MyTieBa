create database tiebadb character set utf8;
use tiebadb;
create table tiezilist(url varchar(300),topic varchar(300),revertnm int(10),pagenm int(10),pgdate date,pgtime time;
create user pub@localhost identified by 'password';
grant all on tiebadb.* to 'pub'@'localhost';