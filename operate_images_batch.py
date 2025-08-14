import requests

# 配置
API_URL = "http://127.0.0.1:5000/add" # 请求接口可选删除/添加
TOKEN = "default_token@add_images123" #token 

# 图片列表
image_urls = [
    "https://huanghunr-blog.oss-cn-hangzhou.aliyuncs.com/website/img/qiaomi1.jpg",
    "https://huanghunr-blog.oss-cn-hangzhou.aliyuncs.com/website/img/qiaomi2.jpg",
    "https://huanghunr-blog.oss-cn-hangzhou.aliyuncs.com/website/img/qiaomi3.jpg",
    # 可以继续添加更多 URL
]

# 图片类型（统一 desktop，也可以根据需求写成列表对应每张图片）
IMAGE_TYPE = "desktop"

for url in image_urls:
    data = {
        "token": TOKEN,
        "url": url,
        "type": IMAGE_TYPE
    }
    try:
        response = requests.post(API_URL, data=data)
        if response.status_code == 200:
            print(f"[成功] {url} -> {response.json()}")
        else:
            print(f"[失败] {url} -> {response.status_code} {response.text}")
    except Exception as e:
        print(f"[异常] {url} -> {e}")
