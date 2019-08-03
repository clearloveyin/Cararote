启动手顺
# linux
1. 使用适当的python
source py36env/bin/activate
2. 使用数据库及表单
python manage.py db init # 没有migrations文件时要执行
python manage.py db migrate
python manage.py db upgrade
python init_db_data.py # 向数据库插入默认数据（例如：状态，角色信息）
3. 在数据库执行下面脚本，生成view
lastest_man_day_id.sql
4. 启动Flask服务器
python start.py