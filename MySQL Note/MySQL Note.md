

[TOC]

### MySQL Note

**sql语言**：Structured Query Language 即结构化查询语言

#### 什么是数据库

数据库软件应称为DBMS(数据库管理系统)。数据库是通过DBMS创建和操纵的容器。数据库可以是保存在硬设备 上的文件，但也可以不是。在很大程度上说，数据库究竟是 文件还是别的什么东西并不重要，因为你**并不直接访问数据库**;你使用的是DBMS，它替你访问数据库。

- 表(table)
>在你将资料放入自己的文件柜时，并不是随便将它们扔进某个抽屉就完
事了，而是在文件柜中创建文件，然后将相关的资料放入特定的文件中。
在数据库领域中，这种文件称为表。表是一种结构化的文件，可用 来存储某种特定类型的数据。表可以保存顾客清单、产品目录，或者其 他信息清单。

- 列(column)
>表由列组成。列中存储着表中某部分的信息。
>理解列的最好办法是将数据库表想象为一个网格。网格中每一列存 储着一条特定的信息。例如，在顾客表中，一个列存储着顾客编号，另 一个列存储着顾客名，而地址、城市、州以及邮政编码全都存储在各自 的列中。

- 行(row)
>表中的数据是按行存储的，所保存的每个记录存储在自己的行内。如果将表想象为网格，网格中垂直的列为表列，水平行为表行。
>例如，顾客表可以每行存储一个顾客。表中的行数为记录的总数。


- 主键(primary key)
>主键一一列(或一组列)，其值能够唯一区分表中每个行。
>表中每一行都应该有可以唯一标识自己的一列(或一组列)。一个顾 客表可以使用顾客编号列，而订单表可以使用订单ID，雇员表可以使用 雇员ID或雇员社会保险号。

- 数据类型(datatype)
> 所容许的数据的类型。每个表列都有相 应的数据类型，它限制(或容许)该列中存储的数据。
>例如，如果列中存储的为数字(或许是订单中的物品数)，则 相应的数据类型应该为数值类型。如果列中存储的是日期、文本、注释、 金额等，则应该用恰当的数据类型规定出来。


#### 使用MySQL

##### SHOW语句
SHOW COLUMNS FROM **(某张表);

>SHOW COLUMNS要求给出一个表名(这个例子中的FROMcustomers)，它对每个字段返回一行，行中包含字段名、数据 类型、是否允许NULL、键信息、默认值以及其他信息(如字段cust_id 的auto_increment)。


**SHOW STATUS**，用于显示广泛的服务器状态信息;
**SHOW CREATE DATABASE和SHOW CREATE TABLE**，分别用来显示创
建特定数据库或表的MySQL语句;
**SHOW GRANTS**，用来显示授予用户(所有用户或特定用户)的安全权限;
**SHOW ERRORS和SHOW WARNINGS**，用来显示服务器错误或警告消息。


####检索数据
##### SELECT语句
>使用SELECT检索表数据，必须至少给出两条信息——想选择什 么，以及从什么地方选择。

检索单个列

    SELECT pro_name FROM products;

检索多个列

     SELECT pro_name，pro_id,pro_price FROM products;
     
检索所有列

     SELECT * FROM products;
>使用通配符 一般，除非你确实需要表中的每个列，否则最 好别使用*通配符。虽然使用通配符可能会使你自己省事，不 用明确列出所需列，但检索不需要的列通常会降低检索和应 用程序的性能。

检索不同的行

    SELECT DISTINCT pro_price FROM products;

>DISTINCT关键字应用于所有列而 不仅是前置它的列。如果给出SELECT DISTINCT vend_id, prod_price，除非指定的两个列都不同，否则所有行都将被 检索出来。

限制结果

    SELECT  pro_name FROM products LIMIT 5;

>带一个值的LIMIT总是从第一行开始，给出的数为返回的行数。 带两个值的LIMIT可以指定从行号为第一个值的位置开始。

>LIMIT语法 LIMIT 3, 4的含义是从行4开始的3 行还是从行3开始的4行?如前所述，它的意思是从行3开始的4 行，这容易把人搞糊涂。

>由于这个原因，MySQL 5支持LIMIT的另一种替代语法。LIMIT 4 OFFSET 3意为从行3开始取4行，就像LIMIT 3, 4一样。

>LIMIT中指定要检索的行数为检索的最大行 数。如果没有足够的行(例如，给出LIMIT 10, 5，但只有13 行)，MySQL将只返回它能返回的那么多行。

使用完全限定的表名

    SELECT  products.pro_name FROM products;




#### 排序检索数据
##### ORDER BY子句

为了明确地排序用SELECT语句检索出的数据，可使用ORDER BY子句。ORDER BY子句取一个或多个列的名字，据此对输出进行排序。

单个排序

    SELECT  pro_name FROM products ORDER BY pro_name;

多个排序

     SELECT  pro_name，pro_price,pro_id FROM products 
     ORDER BY pro_id,pro_name;

指定排序方向

默认升序排序

降序为

     SELECT  pro_name，pro_price,pro_id FROM products 
     ORDER BY pro_price DESC;
>DESC关键字只应用到直接位于其前面的列名。在上例中，只对prod_price列指定DESC，对prod_name列不指定。因此， prod_price列以降序排序，而prod_name列(在每个价格内)仍然按标准 的升序排序。

>在多个列上降序排序 如果想在多个列上进行降序排序，必须 对每个列指定DESC关键字。


#### 过滤数据
##### WHERE子句

数据库表一般包含大量的数据，很少需要检索表中所有行。通常只 会根据特定操作或报告的需要提取表数据的子集。只检索所需数据需要 指定搜索条件(search criteria)，搜索条件也称为过滤条件(filter condition)。

具体匹配

    SELECT  pro_name，pro_price FROM products 
    WHERE pro_id = 5;

范围值查找（BETWEEN）

    SELECT  pro_name，pro_price FROM products 
    WHERE pro_price BETWEEN 5 and 10;


#### 数据过滤
##### 组合WHERE 子句

操作符(operator) 用来联结或改变WHERE子句中的子句的关键 字。也称为逻辑操作符(logical operator)。

**操作符**：and 、or 、in、not
        
    # AND
    SELECT  pro_name，pro_price FROM products 
    WHERE pro_price = 5 AND pro_price = 6;
    # OR
    SELECT  pro_name，pro_price FROM products 
    WHERE pro_price = 5 OR pro_price = 6;


>在WHERE子句中使用圆括号 
>任何时候使用具有and 和 or操作符的WHERE子句，都应该使用圆括号明确地分组操作符。不要过分依赖默认计算次序，即使它确实是你想要的东西也是如 此。使用圆括号没有什么坏处，它能消除歧义。
**SQL(像多数语言一样)在处理OR操作符前，优先处理AND操作符。**

    # IN
    SELECT  pro_name，pro_price FROM products 
    WHERE pro_price IN (5,6,7);
    # NOT
    SELECT  pro_name，pro_price FROM products 
    WHERE pro_price NOT IN (5,6,7);



#### 用通配符进行过滤

通配符(wildcard) 用来匹配值的一部分的特殊字符。
搜索模式(search pattern)由字面值、通配符或两者组合构成的搜索条件。

**百分号(%)通配符**

    SELECT  pro_name，pro_price FROM products 
    WHERE pro_name LIKE 'ab%';
    # %abc%  包含abc的
    # a%b    a开头b结尾
>最常使用的通配符是百分号(%)。在搜索串中，%表示任何字符出现 任意次数。
>此例子使用了搜索模式'j%'。在执行这条子句时，将检索任意以jet起头的词。%告诉MySQL接受jet之后的任意字符，不管它有多少字符。


**下划线(_)通配符**
下划线的用途与%一样，但下划线只匹配单个字符而不是多个字符。


>MySQL的通配符很有用。但这种功能是有代价的:通配 符搜索的处理一般要比前面讨论的其他搜索所花时间更长。


#### 使用正则表达式


- 正则表达式1000|2000。
’|‘ 为正则表达式的OR操作 符。它表示匹配其中之一，因此1000和2000都匹配并返回。

- []是另一种形式的OR语句。
事实上，正则表达式[123]Ton 为[1|2|3]Ton的缩写。

- 正则表达式[1-5] Ton。
[1-5]定义了一个范围，这个表达式意思是匹配1到5，

- . 点 匹配任意字符，因此每个行都被检索出来。

**空白元字符**

![Alt text](./屏幕快照 2018-12-10 下午4.46.02.png)

**字符类**

![Alt text](./屏幕快照 2018-12-10 下午4.44.59.png)

**重复元字符**

![Alt text](./屏幕快照 2018-12-10 下午4.45.09.png)


**定位元字符**
![Alt text](./屏幕快照 2018-12-10 下午4.45.19.png)
