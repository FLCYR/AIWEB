# 文章的表设计
| article_id | title | author | created_at | updated_at | file_name | reading| comments |
|:----------:|:-----:|:------:|:----------:|:----------:|:---------:|:------:|:--------:|
| int primary key auto_increment | varchar(255) | varchar(255) | float | float | varchar(255) | int | int |
> create table articles (article_id int primary key auto_increment, title varchar(255), author varchar(255), created_at float, updated_at float, file_name varchar(255), reading int, comments int);



# 评论的表设计
| comment_id   | parent_id | article_id | user_name |    email     | content | created_at |
|:------------:|:---------:|:----------:|:---------:|:------------:|:-------:|:----------:|
| int primary key auto_increment | int | int | varchar(255) | varchar(128) | text | float |

> create table comments (comment_id int primary key auto_increment, parent_id int, article_id int, user_name varchar(255), email varchar(128),content text, created_at float);

# 用户信息表
| user_id | user_name | sex | created_at | user_desc |
|:-------:|:---------:|:---:|:----------:|:---------:|
| int primary key auto_increment | varchar(255) | int | float | text |
> create table userInfo(user_id int primary key auto_increment,user_name varchar(255),sex int,created_at float,user_desc text);


# 用户Authenticate表=>email 方式
|                id                 |     user_id     | email | password |
|:---------------------------------:|:---------------:|:-----:|:--------:|
| id int primary key auto_increment | int foreign key | text  |   text   |
> create table emailAuth(id int primary key auto_increment,user_id int,email text,password text);