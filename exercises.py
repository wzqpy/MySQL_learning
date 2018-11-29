

mysql -uroot -p   进入私人操作，无密码，点击回车


show databases 显示库

CREATE DATABASE 数据库名 charset utf8;
create database homework charset utf8;

删除表
DROP TABLE 表名;
drop view 表名;

use ****; 选择进入文件库
show tables; 显示库下面的所有表

重点中的重点：关键字的执行优先级
from
where  条件
group by 分组
having  过滤
select 选择
distinct 去重
order by  排序  默认升序，降序 DESC
limit 限制条数

完整性约束
PRIMARY KEY (PK)    标识该字段为该表的主键，可以唯一的标识记录
FOREIGN KEY (FK)    标识该字段为该表的外键
NOT NULL    标识该字段不能为空
UNIQUE KEY (UK)    标识该字段的值是唯一的
AUTO_INCREMENT    标识该字段的值自动增长（整数类型，而且为主键）
DEFAULT    为该字段设置默认值
UNSIGNED 无符号
ZEROFILL 使用0填充

汇聚函数
avg count max min sum 

枚举类型与集合类型(
	字段的值只能在给定范围中选择，如单选框，多选框
enum 单选 只能在给定的范围内选一个值，如性别 sex 男male/女female
set 多选 在给定的范围内可以选择一个或一个以上的值（爱好1,爱好2,爱好3...）)

表连接
select * from A
left join B 
on A.aID = B.bID  对齐A表

right join B   对齐B表
inner join B   相交数据


创建表  老师表
create table teacher(
tid int not null auto_increment,
tname varchar(10) not null,
primary key (tid)
);

插入数据
INSERT INTO teacher values
(1,'张三'),
(2,'李四'),
(3,'王五');

INSERT INTO teacher(tname) values
(1,'张三'),
(2,'李四'),
(3,'王五');

删除单行数据
delete from teacher
where tid = 4;

创建表 课程表
create table course(
cid int not null primary key auto_increment,
cname varchar(10),
teacher_id int not null,
foreign key(teacher_id) references teacher(tid)
on delete cascade
on update cascade
);

插入数据
insert into course(cname,teacher_id) values
('生物',1),
('体育',1),
('物理',2);


创建年级表
create table class_grade(
gid int not null primary key auto_increment,
gname varchar(10) not null
);

插入数据
insert into class_grade(gname) values
('一年级')，
('二年级')，
('三年级');

创建班级表
create table class(
cid int not null primary key auto_increment,
caption varchar(10) not null,
grade_id int not null,
foreign key(grade_id) references class_grade(gid)
on delete cascade
on update cascade
);

插入数据
insert into class(caption,grade_id) values
('一年一班',1),
('二年一班',2),
('三年二班',3);

创建学生表
create table student(
sid int not null primary key auto_increment,
sname varchar(10) not null,
gender enum('男','女'),
class_id int not null,
foreign key(class_id) references class(cid)
on delete cascade
on update cascade
);

插入数据
insert into student(sname,gender,class_id) values
('乔丹','女',1),
('艾佛森','女',1),
('科比','男',2);

创建成绩表
create table score(
sid int not null primary key auto_increment,
student_id int not null,
course_id int not null,
score int not null,
foreign key(student_id) references student(sid)
on delete cascade
on update cascade,
foreign key(course_id) references course(cid)
on delete cascade
on update cascade
);
插入数据
insert into score(student_id,course_id,score) values
(1,1,60),
(1,2,59),
(2,2,99);

创建班级任职表
create table teach2cls(
tcid int not null primary key auto_increment,
tid int not null,
cid int not null,
foreign key(tid) references teacher(tid)
on delete cascade
on update cascade,
foreign key(cid) references class(cid)
on delete cascade
on update cascade
);
插入数据
insert into teach2cls(tid,cid) values
(1,1),
(1,2),
(2,1),
(3,2);

1、自行创建测试数据；

2、查询学生总人数；
select count(sid) as student_sum from student;
#聚集函数 count(*)

3、查询“生物”课程和“物理”课程成绩都及格的学生id和姓名；
select sid,sname from student
where sid in(select student_id from score
where score >=60 and (course_id =1 or course_id =3));
#多表子查询

4、查询每个年级的班级数，取出班级数最多的前三个年级；
select caption,count(*) from class
group by grade_id DESC
limit 3;
#分组 降序

5、查询平均成绩最高和最低的学生的id和姓名以及平均成绩；


select * from 
(select score.sid,avg(score) as avgscore,sname from score,student
where score.student_id = student.sid
group by student_id
limit 1) as t1,
(select score.sid,avg(score) as avgscore,sname from score,student
where score.student_id = student.sid
group by student_id DESC
limit 1) as t2;



6、查询每个年级的学生人数；

思路：生成一个学生关联班级，班级关联年级，然后通过年级分类，计算年级下的人数
select count(gid),gid from class_grade,class,student
where class_grade.gid = class.grade_id
and class.cid = student.class_id
group by gid;


7、查询每位学生的学号，姓名，选课数，平均成绩；
  
思路：关键字（每位学生），成绩有几门选课数就是几

select student.sid,sname,count(student_id),avg(score) from student,score
where student.sid = score.student_id
group by student_id;


8、查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名、成绩最低的课程名及分数；

思路：运用了concat 

select sname,concat(max(score),cname),concat(min(score),cname) from student,score,course
where student.sid = 1 
and student.sid = score.student_id
and score.course_id = course.cid
group by score.student_id;


9、查询姓“李”的老师的个数和所带班级数；

思路：用通配符进行过滤查询 

select tname,count(tname),count(cid) from teacher,teache2cls
where tname like '李%'
and teacher.tid = teache2cls.tid
group by teache2cls.tid;


10、查询班级数小于5的年级id和年级名；

思路： having 过滤 

select gid,gname,count(grade_id) from class_grade,class 
where class.grade_id = class_grade.gid
group by grade_id
having count(grade_id) < 5;




11、查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)，示例结果如下；


知识点： case when

select cid,caption,grade_id,
case when grade_id between 1 and 2 then "低年级"
when grade_id between 3 and 4 then "中年级"
when grade_id between 5 and 6 then "高年级"
else 0 end as '年级级别'
from class;




12、查询学过“张三”老师2门课以上的同学的学号、姓名；


select sid,sname from student
where sid in(
select student_id from score
where course_id in(
select cid from teacher,course
where teacher.tname = '张三'
and teacher.tid = course.teacher_id)
group by student_id
having count(student_id)>=2);



13、查询教授课程超过2门的老师的id和姓名

select tid,tname from teacher
where tid in(
select teacher_id from course
group by teacher_id
having count(teacher_id) >2);


14、查询学过编号“1”课程和编号“2”课程的同学的学号、姓名；

select sid,sname from student
where sid in(
select student_id from score
where student_id = 1
or student_id = 2);



15、查询没有带过高年级的老师id和姓名；



select tid,tname from teacher
where tid not in(
select tid from teach2cls
where cid in(
select t1.cid from(
select class.cid,class.caption,class_grade.gname,
case
when class_grade.gid between 1 and 2 then '低年级'
when class_grade.gid between 3 and 4 then '中年级'
when class_grade.gid between 5 and 6 then '高年级' else 0 end as grade_layer
from class,class_grade
where class.grade_id=class_grade.gid)as t1
where t1.grade_layer='高'));


16、查询学过“张三”老师所教的所有课的同学的学号、姓名；


select sid,sname from student
where sid in(
select student_id from score
where course_id in(
select cid from course
inner join teacher
on course.teacher_id = teacher.tid
where teacher.tname = '张三'));



17、查询带过超过2个班级的老师的id和姓名；

select tid,tname from teacher
where tid in(
select tid from teache2cls
group by tid
having count(cid)>2);



18、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；



select sid,sname from student
where sid in(
select t1.student_id from
(select student_id,score from score
where course_id = 2) as t1,
(select student_id,score from score
where course_id = 1) as t2
where t1.score < t2.score);



19、查询所带班级数最多的老师id和姓名；


select tid,tname from teacher
where tid =(
select tid from teache2cls
group by tid
order by count(cid) desc
limit 1);




20、查询有课程成绩小于60分的同学的学号、姓名；

select sid,sname from student
where sid in(
select student_id from score
where score<60);


21、查询没有学全所有课的同学的学号、姓名；


select sid,sname from student
where sid not in(
select student_id from score
group by student_id
having count(course_id) =(
select count(cid) from course));



22、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名；

select sid,sname from student
where sid in(
select student_id from score
where course_id in (
select course_id from score
where student_id= 1))
and sid != 1;



23、查询至少学过学号为“1”同学所选课程中任意一门课的其他同学学号和姓名；









24、查询和“2”号同学学习的课程完全相同的其他同学的学号和姓名；

关键字：完全相同  
思路：对课程数计数

select sid,sname from student
where sid in(
select t1.student_id from
(select student_id,course_id,count(course_id) as course1 from score
where student_id != 2) as t1
inner join
(select student_id,course_id,count(course_id) as course2 from score
where student_id = 2
group by course_id) as t2
on t1.course_id = t2.course_id
and t1.course1 = t2.course2);



25、删除学习“张三”老师课的score表记录；


delete from  score 
where course_id in(
select course.cid from course,teacher
where course.teacher_id = teacher.tid
and teacher.tname = '张三');


26、向score表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“2”课程的同学学号；②插入“2”号课程的平均成绩；








27、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 学生ID,语文,数学,英语,有效课程数,有效平均分；

思路：生成 每科成绩的表，然后连接 

# select student_id,course_id,score from score 
# where course_id in 
# (select cid from course
# where cname = '生物');


# select student_id,course_id,score from score 
# where course_id in 
# (select cid from course
# where cname = '体育');


# select student_id,course_id,score from score 
# where course_id in 
# (select cid from course
# where cname = '物理');





28、查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；

select t1.cid,max(score),min(score) from score
right join
(select cid from course) as t1
on score.course_id = t1.cid
group by t1.cid;



29、按各科平均成绩从低到高和及格率的百分数从高到低顺序；


知识点： case when 


select t1.cid,avg(score) as avgscore,
sum(case when score.score>60 then 1 else 0 end)/count(1)*100 as percent from score
right join
(select cid from course) as t1
on score.course_id = t1.cid
group by t1.cid
order by avgscore,
percent desc;




30、课程平均分从高到低显示（显示任课老师）；

思路： 右连接后在联结2张表

select t1.course_id,t1.avgscore,tname from teacher,
(select course_id,avg(score) as avgscore from score
right join teacher
on teacher.tid = score.course_id
group by course_id desc) as t1
where t1.course_id = teacher.tid;  #(注意这个条件)





31、查询各科成绩前三名的记录(不考虑成绩并列情况)

关键字：每科。成绩








32、查询每门课程被选修的学生数；


select cid,cname,countstudent from course
left join
(select count(student_id) as countstudent,course_id from score
group by course_id) as t1
on course.cid = t1.course_id;




33、查询选修了2门以上课程的全部学生的学号和姓名；


select * from student
where sid in(
select student_id from score 
group by student_id
having count(course_id)>=2);



34、查询男生、女生的人数，按倒序排列；

select gender,count(sid) from student
group by gender desc;


35、查询姓“张”的学生名单；


select sname from student
where sname like '张%';




36、查询同名同姓学生名单，并统计同名人数；

思路：同名同姓 对名字分组

select sid,sname,count(sname) as count_sname 
from student
group by sname 
order by sid;



37、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；



select cid,cname,avg(score) as avgscore from
(select score,cid,cname from score
right join course
on course.cid = score.course_id) as t1
group by cid
order by avgscore,
cid desc;




38、查询课程名称为“数学”，且分数低于60的学生姓名和分数；

思路：没得数学 用 生物 测试

select sname,score from student
right join
(select student_id,score from score
where course_id in(
select cid from course
where cname = '生物')) as t1
on t1.student_id = student.sid
having score <= 60;



39、查询课程编号为“3”且课程成绩在80分以上的学生的学号和姓名；

思路：用课程2 测试

select sid,sname,score from student,
(select student_id,score from score
where course_id = 2
having score > 80) as t1
where student.sid = t1.student_id;



40、求选修了课程的学生人数

思路：有成绩就选修

select count(*) as countstudent from
(select distinct sname as name from score
right join student
on score.student_id = student.sid) as t1;



41、查询选修“王五”老师所授课程的学生中，成绩最高和最低的学生姓名及其成绩；

测试老师用 张三

select * from score
right join 
select cid from course
where teacher_id in(
select tid from teacher
where tname = '张三') as t1
on score.course_id = t1.cid;




42、查询各个课程及相应的选修人数；



select cid,cname,count(student_id) from
(select * from score
right join course
on course.cid = score.course_id) as t1
group by cid;




43、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；




select s1.student_id from 
score as s1,
score as s2
where s1.student_id != s2.student_id
and s1.course_id != s2.course_id
and s1.score = s2.score;




44、查询每门课程成绩最好的前两名学生id和姓名；



# select * from score
# right join course
# on score.course_id = course.cid;






45、检索至少选修两门课程的学生学号；



select student_id from score
having count(student_id)>2;



46、查询没有学生选修的课程的课程号和课程名；

select course_id from score
where course_id not in(
select cid from course);




47、查询没带过任何班级的老师id和姓名；


select tid,tname from teacher
where teacher.tid not in(
select tid from teach2cls);




48、查询有两门以上课程超过80分的学生id及其平均成绩；


select student_id,avg(score) from score
where score> 80
group by student_id
having count(score)>=2;




49、检索“3”课程分数小于60，按分数降序排列的同学学号；


select student_id from score
where course_id = 3 and score <60
order by student_id desc;



50、删除编号为“2”的同学的“1”课程的成绩；



delete score from score 
where student_id=2 and course_id=1;



51、查询同时选修了物理课和生物课的学生id和姓名；

测试用生物和体育

select * from student
inner join
(select student_id,course_id from score
where course_id in (
select cid from course
where cname in ('生物','体育'))
group by student_id
having count(course_id) = 2 ) as t1
on student.sid = t1.student_id;





