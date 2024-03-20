from openai import OpenAI

if __name__ == '__main__':
    openai_api_key = "EMPTY"
    openai_api_base = "http://172.16.2.83:8012/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    response = client.chat.completions.create(
        model='Qwen/Qwen-Chat',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        # temperature=self.temperature,
        stream=True,
        # top_p=self.top_p,
        # max_tokens=self.token_upper_limit,
        extra_body={
            'repetition_penalty': 1,
        }
    )

    if response is not None:
        partial_text = ""
        for chunk in response:
            new_text = (chunk.choices[0].delta.content or "")
            print(new_text, end="", flush=True)
            partial_text += new_text
            # yield partial_text
    else:
        pass
