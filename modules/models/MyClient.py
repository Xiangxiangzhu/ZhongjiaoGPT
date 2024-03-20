import os
import json
from openai import OpenAI
import logging
import colorama
from .base_model import BaseLLMModel
from ..presets import *


class QwenClient(BaseLLMModel):
    def __init__(self, model_name, user_name="") -> None:
        super().__init__(model_name=model_name, user=user_name)

        openai_api_key = "EMPTY"
        openai_api_base = "http://172.16.2.83:8012/v1"

        self.client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )

        response = self.client.chat.completions.create(
            model='Qwen/Qwen-Chat',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ],
            temperature=self.temperature,
            stream=False,
            top_p=self.top_p,
            max_tokens=self.token_upper_limit,
            extra_body={
                'repetition_penalty': 1,
                # 'stop_token_ids': [7]
                # 'stop_token_ids': [151643]
            }

        )
        content = response.choices[0].message.content

    def generation_config(self):
        pass
        # return GenerationConfig.from_dict({
        #     "chat_format": "chatml",
        #     "do_sample": True,
        #     "eos_token_id": 151643,
        #     "max_length": self.token_upper_limit,
        #     "max_new_tokens": 512,
        #     "max_window_size": 6144,
        #     "pad_token_id": 151643,
        #     "top_k": 0,
        #     "top_p": self.top_p,
        #     "transformers_version": "4.33.2",
        #     "trust_remote_code": True,
        #     "temperature": self.temperature,
        # })

    def get_answer_at_once(self):
        response = self.client.chat.completions.create(
            model='Qwen/Qwen-Chat',
            messages=self.history,
            temperature=self.temperature,
            stream=False,
            top_p=self.top_p,
            max_tokens=self.token_upper_limit,
            extra_body={
                'repetition_penalty': 1,
                # 'stop_token_ids': [7]
                # 'stop_token_ids': [151643]
            }
        )
        content = response.choices[0].message.content
        return content, len(content)

    def get_answer_stream_iter(self):
        response = self.client.chat.completions.create(
            model='Qwen/Qwen-Chat',
            messages=self.history,
            temperature=self.temperature,
            stream=True,
            top_p=self.top_p,
            max_tokens=self.token_upper_limit,
            extra_body={
                'repetition_penalty': 1,
                # 'stop_token_ids': [7]
                # 'stop_token_ids': [151643]
            }
        )

        if response is not None:
            partial_text = ""
            for chunk in response:
                new_text = (chunk.choices[0].delta.content or "")
                print(new_text, end="", flush=True)
                partial_text += new_text
                yield partial_text
        else:
            pass

        # if response is not None:
        #     iter = self._decode_chat_response(response)
        #     partial_text = ""
        #     for i in iter:
        #         partial_text += i
        #         yield partial_text
        # else:
        #     yield STANDARD_ERROR_MSG + GENERAL_ERROR_MSG
