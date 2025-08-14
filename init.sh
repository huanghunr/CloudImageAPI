#!/bin/bash
set -e

# 启动 PostgreSQL
service postgresql start

# 初始化数据库和用户
su - postgres -c "psql -c \"CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';\""
su - postgres -c "psql -c \"CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};\""

# 导入初始化数据
su - postgres -c "psql ${DB_NAME} < /init.sql"

# 修改表所有者
su - postgres -c "psql -d ${DB_NAME} -c \"ALTER TABLE images OWNER TO ${DB_USER};\""

# 启动 Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:5000 app:app
