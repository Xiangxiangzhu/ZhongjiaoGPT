import requests
import json
import traceback


def decode_chat_response(self, response):
    error_msg = ""
    for chunk in response.iter_lines():
        if chunk:
            chunk = chunk.decode()
            chunk_length = len(chunk)
            try:
                chunk = json.loads(chunk[6:])
            except:
                print("JSON解析错误,收到的内容: " + f"{chunk}")
                error_msg += chunk
                continue
            try:
                if chunk_length > 6 and "delta" in chunk["choices"][0]:
                    if "finish_reason" in chunk["choices"][0]:
                        finish_reason = chunk["choices"][0]["finish_reason"]
                    else:
                        finish_reason = chunk["finish_reason"]
                    if finish_reason == "stop":
                        break
                    try:
                        yield chunk["choices"][0]["delta"]["content"]
                    except Exception as e:
                        # logging.error(f"Error: {e}")
                        continue
            except:
                print(f"ERROR: {chunk}")
                continue
    if error_msg and not error_msg == "data: [DONE]":
        raise Exception(error_msg)




if __name__ == '__main__':
    openai_api_key = "EMPTY"
    openai_api_base = "http://172.16.2.83:8012/v1"

    # 构造请求URL和请求头部
    url = f"{openai_api_base}/chat/completions"
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
        "stream": False,
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

    print("##############")
    print(response)
    print("##############")

    response = json.loads(response.text)
    content = response["choices"][0]["message"]["content"]
    total_token_count = response["usage"]["total_tokens"]

    print(content)
    print('######')
    print(total_token_count)

    # print(response)
    #
    # if response:
    #     partial_text = ""
    #     # 由于设置了stream=True，我们可以逐步读取响应
    #     for line in response.iter_lines():
    #         if line:
    #             decoded_line = line.decode('utf-8')
    #             print(decoded_line)
    #             partial_text += decoded_line
    #             # yield partial_text  # 如果你需要在函数中使用yield
    # else:
    #     traceback.print_exc()
    #     print("No response or error.")




