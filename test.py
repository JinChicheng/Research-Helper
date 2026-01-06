import requests

API_KEY = "sk-ijejcfkbxjkjngqcywnribltbizwlghpbgwxsldpiybztqyx"
ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 核心修正：用 messages 字段，格式为包含角色和内容的数组
data = {
    "model": "deepseek-ai/DeepSeek-R1",  # 确保模型名称正确
    "messages": [
        {"role": "user", "content": "你是谁"}  # user 表示用户的提问
    ]
}

response = requests.post(
    ENDPOINT,
    headers=headers,
    json=data
)

print(response.status_code, response.text)