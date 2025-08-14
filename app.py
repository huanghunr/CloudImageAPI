from flask import Flask, request, jsonify, redirect
import psycopg2
import random
import os

app = Flask(__name__)

# ====== 配置部分 ======
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "image_api")
DB_USER = os.getenv("DB_USER", "img_user")
DB_PASS = os.getenv("DB_PASS", "你的数据库密码")

# 用于添加图片的密钥（最好放在环境变量里）
ADD_IMAGE_TOKEN = os.getenv("ADD_IMAGE_TOKEN", "你的安全密钥")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

@app.route("/add", methods=["GET"])
def add_image():
    """
    获取图片链接添加到数据库中
    """
    token = request.args.get("token")
    if token != ADD_IMAGE_TOKEN:
        return jsonify({"error": "无效的 token"}), 403

    url = request.args.get("url")
    img_type = request.args.get("type", "desktop")  # 默认为 desktop

    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    if img_type not in ["android", "desktop"]:
        return jsonify({"error": "type 只能是 android 或 desktop"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO images (url, type) VALUES (%s, %s)", (url, img_type))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "添加成功", "url": url, "type": img_type})


@app.route("/random-image", methods=["GET"])
def random_image():
    """
    获取图片链接并重定向到图片链接
    """
    img_type = request.args.get("type", "desktop")
    if img_type not in ["android", "desktop"]:
        return jsonify({"error": "type 只能是 android 或 desktop"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT url FROM images WHERE type = %s", (img_type,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return jsonify({"error": f"数据库中没有 {img_type} 类型的图片"}), 404

    url = random.choice(rows)[0]
    return redirect(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
