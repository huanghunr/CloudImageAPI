
# CloudImageAPI

一个基于 Flask + PostgreSQL 的随机图片 API，专用于将**云存储（OSS、图床等）图片链接**添加到数据库，并提供随机图片接口，可根据终端类型（desktop / mobile）返回不同大小的图片链接。
可用于壁纸 API、图床图片随机展示等场景。

---

## 🚀 功能概览

* **/add** → 添加图片（POST）
* **/delete** → 删除图片（POST）
* **/list** → 获取所有图片信息（POST）
* **/random-image** → 获取随机图片链接并跳转（GET）

---

## 📦部署方式

### 1.克隆项目
```bash
git clone https://github.com/huanghunr/CloudImageAPI.git
cd CloudImageAPI
```
### 2.配置密钥
请在 dockerfile 文件中，修改你的数据库密钥和安全密钥。
默认为
```
DB_PASS=img_user@SQL123  #数据库密钥
ADD_IMAGE_TOKEN=default_token@add_images123 #验证token
```
dockerfile
```
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
ENV API_TOKEN=default_token@add_images123

EXPOSE 5000

RUN chmod +x /init.sh

CMD ["/init.sh"]

```
### 3.运行容器
```bash
docker build --pull --rm -f 'dockerfile' -t 'cloudimageapi:latest' '.' 
docker run --rm -d -p 5000:5000/tcp cloudimageapi:latest 
```
---

## 📌 API 使用说明

### 1. 添加图片

* **接口**：`/add`

* **方法**：`POST`

* **参数**：

  | 参数名   | 必填 | 说明                                       |
  | ----- | -- | ---------------------------------------- |
  | token | ✅  | API 安全密钥                                 |
  | url   | ✅  | 图片链接                                     |
  | type  | ❌  | 图片类型（`android` 或 `desktop`，默认 `desktop`） |

* **示例**：

```bash
curl -X POST http://127.0.0.1:5000/add \
     -F "token=你的安全密钥" \
     -F "url=https://example.com/image.jpg" \
     -F "type=desktop"
```

* **返回**：

```json
{
    "message": "添加成功",
    "url": "https://example.com/image.jpg",
    "type": "desktop"
}
```

---

### 2. 删除图片

* **接口**：`/delete`

* **方法**：`POST`

* **参数**：

  | 参数名   | 必填 | 说明               |
  | ----- | -- | ---------------- |
  | token | ✅  | API 安全密钥         |
  | id    | ❌  | 图片 ID（与 url 二选一） |
  | url   | ❌  | 图片 URL（与 id 二选一） |

* **示例（按 ID 删除）**：

```bash
curl -X POST http://127.0.0.1:5000/delete \
     -F "token=你的安全密钥" \
     -F "id=3"
```

* **示例（按 URL 删除）**：

```bash
curl -X POST http://127.0.0.1:5000/delete \
     -F "token=你的安全密钥" \
     -F "url=https://example.com/image.jpg"
```

* **返回**：

```json
{
    "message": "删除成功",
    "deleted_count": 1
}
```

---

### 3. 获取所有图片列表

* **接口**：`/list`

* **方法**：`POST`

* **参数**：

  | 参数名   | 必填 | 说明       |
  | ----- | -- | -------- |
  | token | ✅  | API 安全密钥 |

* **示例**：

```bash
curl -X POST http://127.0.0.1:5000/list \
     -F "token=你的安全密钥"
```

* **返回**：

```json
{
    "count": 3,
    "images": [
        {"id": 1, "url": "https://example.com/a.jpg", "type": "desktop"},
        {"id": 2, "url": "https://example.com/b.jpg", "type": "android"},
        {"id": 3, "url": "https://example.com/c.jpg", "type": "desktop"}
    ]
}
```

---

### 4. 获取随机图片链接并跳转

* **接口**：`/random-image`

* **方法**：`GET`

* **参数**：

  | 参数名  | 必填 | 说明                                       |
  | ---- | -- | ---------------------------------------- |
  | type | ❌  | 图片类型（`android` 或 `desktop`，默认 `desktop`） |

* **示例**：

```bash
curl "http://127.0.0.1:5000/random-image?type=desktop"
```

* **返回**：

  * 直接 **302 重定向** 到随机图片 URL

---
