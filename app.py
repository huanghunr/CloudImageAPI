from flask import Flask, request, jsonify, redirect
import psycopg2
import random
import os
import hmac
from functools import wraps
from urllib.parse import urlparse

app = Flask(__name__)

# 获取环境变量
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# 用于认证的密钥
API_TOKEN = os.getenv("API_TOKEN")

# 受信任的图片链接
ALLOWED_DOMAINS = ["static.example.com"]

# 数据库连接
def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

# Token 验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.form.get("token")
        if not token or not hmac.compare_digest(token, API_TOKEN):
            return jsonify({"error": "无效的 token"}), 403
        return f(*args, **kwargs)
    return decorated

# 添加图片
@app.route("/add", methods=["POST"])
@token_required
def add_image():
    url = request.form.get("url")
    img_type = request.form.get("type", "desktop")

    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    
    # 验证添加的url是否可信
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme in ["http", "https"] or parsed_url.hostname not in ALLOWED_DOMAINS:
            return jsonify({"error": "URL 域名不被允许"}), 400
    except Exception:
        return jsonify({"error": "无效的 URL 格式"}), 400
    
    if img_type not in ["mobile", "desktop"]:
        return jsonify({"error": "type 只能是 mobile 或 desktop"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO images (url, type) VALUES (%s, %s)", (url, img_type))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "添加成功", "url": url, "type": img_type})

# 删除图片
@app.route("/delete", methods=["POST"])
@token_required
def delete_image():
    img_id = request.form.get("id")
    url = request.form.get("url")

    if not img_id and not url:
        return jsonify({"error": "必须提供 id 或 url"}), 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        if img_id:
            cur.execute("DELETE FROM images WHERE id = %s", (img_id,))
        elif url:
            cur.execute("DELETE FROM images WHERE url = %s", (url,))
        deleted_count = cur.rowcount
        conn.commit()

        if deleted_count == 0:
            return jsonify({"message": "未找到符合条件的图片"}), 404
        else:
            return jsonify({"message": "删除成功", "deleted_count": deleted_count})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# 获取所有图片
@app.route("/list", methods=["POST"])
@token_required
def list_images():
    # 从请求中获取分页参数，提供默认值
    page = request.form.get("page", 1, type=int)
    per_page = request.form.get("per_page", 20, type=int)
    offset = (page - 1) * per_page

    conn = get_conn()
    cur = conn.cursor()

    try:
        # 使用 LIMIT 和 OFFSET 来分页查询
        cur.execute(
            "SELECT id, url, type FROM images ORDER BY id ASC LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        rows = cur.fetchall()

        # 获取总条目数，用于返回给前端
        cur.execute("SELECT COUNT(*) FROM images")
        total_count = cur.fetchone()[0]

        images = [
            {"id": r[0], "url": r[1], "type": r[2]}
            for r in rows
        ]

        return jsonify({
            "total_count": total_count,
            "page": page,
            "images": images
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# 获取随机图片（GET）
@app.route("/random-image", methods=["GET"])
def random_image():
    img_type = request.args.get("type", "desktop")
    if img_type not in ["mobile", "desktop"]:
        return jsonify({"error": "type 只能是 mobile 或 desktop"}), 400

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
