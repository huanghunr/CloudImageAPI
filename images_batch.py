import requests

# 配置
API_BASE = "http://127.0.0.1:5000"
API_URL = f"{API_BASE}/add"  # 改成 "/delete" 即执行批量删除
TOKEN = "default_token@add_images123"

# 添加图片列表（仅当 API_URL 为 /add 时生效）
image_urls = [
    "https://exa.com/img/1.jpg",
]

IMAGE_TYPE = "desktop"  # 可按需改成每张图片不同类型

# 删除图片列表（仅当 API_URL 为 /delete 时生效，可以使用id或者url）
delete_list = [9999, 99999, "https://exa.com/img/3.jpg"]

def batch_add():
    for url in image_urls:
        data = {"token": TOKEN, "url": url, "type": IMAGE_TYPE}
        try:
            response = requests.post(API_URL, data=data)
            if response.status_code == 200:
                print(f"添加成功 {url} -> {response.json()}")
            else:
                print(f"添加失败 {url} -> {response.status_code} {response.text}")
        except Exception as e:
            print(f"错误 {url} -> {e}")


def batch_delete():
    for item in delete_list:
        if isinstance(item, int):
            data = {"token": TOKEN, "id": item}
        elif isinstance(item, str):
            data = {"token": TOKEN, "url": item}
        else:
            print(f"跳过 不支持类型 {type(item)} -> {item}")
            continue

        try:
            response = requests.post(API_URL, data=data)
            if response.status_code == 200:
                print(f"删除成功 {item} -> {response.json()}")
            else:
                print(f"删除失败 {item} -> {response.status_code} {response.text}")
        except Exception as e:
            print(f"错误 {item} -> {e}")

if __name__ == "__main__":
    if API_URL.endswith("/add"):
        batch_add()
    elif API_URL.endswith("/delete"):
        batch_delete()
    else:
        print("请把 API_URL 设置为 /add 或 /delete")
