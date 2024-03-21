import requests
import json
import traceback

if __name__ == '__main__':
    openai_api_key = "EMPTY"
    openai_api_base = "http://172.16.2.83:8012/v1"

    # 构造请求URL和请求头部
    url = f"{openai_api_base}/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    # 构造请求的正文（body）
    data = {
        "model": 'Qwen/Qwen-Chat',
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        "stream": True,
        "extra_body": {
            'repetition_penalty': 1,
        }
    }

    # 确保不使用代理
    proxies = {
        "http": None,
        "https": None,
    }

    # 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies, stream=False)
    # content = response["choices"][0]["message"]["content"]

    print(response)

    if response:
        partial_text = ""
        # 由于设置了stream=True，我们可以逐步读取响应
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
                partial_text += decoded_line
                # yield partial_text  # 如果你需要在函数中使用yield
    else:
        traceback.print_exc()
        print("No response or error.")
