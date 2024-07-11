# Readme

## 项目名称：购物网站及其管理系统

## 作者信息：

| 姓名   | 学号     |
| ------ | -------- |
| 魏嘉灼 | 21307045 |
| 马俊杰 | 21307017 |
| 马逢睿 | 21307055 |
| 梁权锋 | 21307054 |
| 梁智钊 | 21307024 |

## 文件框架

项目代码全部位于software文件夹中：

/software/static：静态文件，包括前端的CSS、JS样式等，同时存储商品图片；

/mydatabase/templates：网页html代码

/mydatabase/app.py：后端Flask代码

/mydatabase/database.py：操作数据库代码

/mydatabase/database.sql：创建数据库的SQL代码

/mydatabase/goods.sql：添加基础商品信息

## 运行项目：

项目使用postgreSQL，使用前请先配置数据库；
```bash
su postgres
psql
CREATE DATABASE mydatabase;
\t /home/ubuntu/software/mydatabase/database.sql
\t /home/ubuntu/software/mydatabase/goods.sql
```

配置环境
```bash
cd ./emall
conda create -n software python=3.9
conda activate software
pip install -r requirements.txt
npm install
```

运行
```bash
python app.py
```

测试
```bash
cd ./software
export PYTHONPATH=/home/ubuntu/software
pytest
```

test 3
test 4
test 5
test 6