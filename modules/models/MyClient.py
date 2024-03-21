import os
import json
import requests
import traceback
from openai import OpenAI
import logging
import colorama
from ..config import retrieve_proxy
from .base_model import BaseLLMModel
from ..presets import *
from ..utils import construct_system


class MyBaseClient(BaseLLMModel):
    def __init__(self, model_name, user_name="") -> None:
        super().__init__(model_name=model_name, user=user_name)

        openai_api_key = "EMPTY"
        openai_api_base = "http://172.16.2.83:8012/v1"

        os.environ.pop('http_proxy', None)
        os.environ.pop('https_proxy', None)
        os.environ.pop('all_proxy', None)

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
        print("##### test ######")
        print(content)
        print("##### test ######")

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


class MyCurlClient(BaseLLMModel):
    def __init__(
            self,
            model_name,
            system_prompt=INITIAL_SYSTEM_PROMPT,
            temperature=1.0,
            top_p=1.0,
            user_name=""
    ) -> None:
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            system_prompt=system_prompt,
            user=user_name
        )
        self.api_key = "EMPTY"
        self.api_base = "http://172.16.2.83:8012/v1/chat/completions"

        self.need_api_key = False
        self._refresh_header()

    def get_answer_stream_iter(self):
        if not self.api_key:
            raise Exception(NO_APIKEY_MSG)
        response = self._get_response(stream=True)
        if response is not None:
            iter = self._decode_chat_response(response)
            partial_text = ""
            for i in iter:
                partial_text += i
                yield partial_text
        else:
            yield STANDARD_ERROR_MSG + GENERAL_ERROR_MSG

    def get_answer_at_once(self):
        if not self.api_key:
            raise Exception(NO_APIKEY_MSG)
        response = self._get_response()
        response = json.loads(response.text)
        content = response["choices"][0]["message"]["content"]
        total_token_count = response["usage"]["total_tokens"]
        return content, total_token_count

    def _refresh_header(self):
        openai_api_key = "EMPTY"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }

    def _get_response(self, stream=False):
        openai_api_key = "EMPTY"
        system_prompt = self.system_prompt
        history = self.history
        logging.debug(colorama.Fore.YELLOW +
                      f"{history}" + colorama.Fore.RESET)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }

        if system_prompt is not None:
            history = [construct_system(system_prompt), *history]

        payload = {
            "model": self.model_name,
            "messages": history,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n_choices,
            "stream": stream,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
        }

        if self.max_generation_token is not None:
            payload["max_tokens"] = self.max_generation_token
        if self.stop_sequence is not None:
            payload["stop"] = self.stop_sequence
        if self.logit_bias is not None:
            payload["logit_bias"] = self.encoded_logit_bias()
        if self.user_identifier:
            payload["user"] = self.user_identifier

        if stream:
            timeout = TIMEOUT_STREAMING
        else:
            timeout = TIMEOUT_ALL

        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""
        with retrieve_proxy(""):
            try:
                response = requests.post(
                    self.api_base,
                    headers=headers,
                    json=payload,
                    stream=stream,
                    timeout=timeout,
                )
            except:
                traceback.print_exc()
                return None
        return response

    @staticmethod
    def _decode_chat_response(response):
        error_msg = ""
        for chunk in response.iter_lines():
            if chunk:
                chunk = chunk.decode()
                chunk_length = len(chunk)
                try:
                    chunk = json.loads(chunk[6:])
                except:
                    print(i18n("JSON解析错误,收到的内容: ") + f"{chunk}")
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
