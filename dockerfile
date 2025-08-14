FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt &&\
    apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

COPY init.sql /init.sql
COPY app.py /app/app.py
COPY init.sh /init.sh

# 设置环境变量
ENV DB_HOST=127.0.0.1
ENV DB_PORT=5432
# 你的数据库名称、用户名，默认即可
ENV DB_NAME=image_api
ENV DB_USER=img_user
# 你的数据库密码，尽量使用更复杂的密码
ENV DB_PASS=img_user@SQL123
# 你的安全密钥，用于添加图片/删除图片/列出图片的验证
ENV ADD_IMAGE_TOKEN=default_token@add_images123

EXPOSE 5000

RUN chmod +x /init.sh

CMD ["/init.sh"]
