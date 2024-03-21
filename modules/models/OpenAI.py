from __future__ import annotations

import json
import logging
import traceback

import colorama
import requests

from .. import shared
from ..config import retrieve_proxy, sensitive_id, usage_limit, http_proxy, https_proxy
from ..index_func import *
from ..presets import *
from ..utils import *
from .base_model import BaseLLMModel


class OpenAIClient(BaseLLMModel):
    def __init__(
            self,
            model_name,
            api_key,
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
        self.api_key = api_key
        self.need_api_key = True
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

    def count_token(self, user_input):
        input_token_count = count_token(construct_user(user_input))
        if self.system_prompt is not None and len(self.all_token_counts) == 0:
            system_prompt_token_count = count_token(
                construct_system(self.system_prompt)
            )
            return input_token_count + system_prompt_token_count
        return input_token_count

    def billing_info(self):
        try:
            curr_time = datetime.datetime.now()
            last_day_of_month = get_last_day_of_month(
                curr_time).strftime("%Y-%m-%d")
            first_day_of_month = curr_time.replace(day=1).strftime("%Y-%m-%d")
            usage_url = f"{shared.state.usage_api_url}?start_date={first_day_of_month}&end_date={last_day_of_month}"
            try:
                usage_data = self._get_billing_data(usage_url)
            except Exception as e:
                # logging.error(f"获取API使用情况失败: " + str(e))
                if "Invalid authorization header" in str(e):
                    return i18n("**获取API使用情况失败**，需在填写`config.json`中正确填写sensitive_id")
                elif "Incorrect API key provided: sess" in str(e):
                    return i18n("**获取API使用情况失败**，sensitive_id错误或已过期")
                return i18n("**获取API使用情况失败**")
            # rounded_usage = "{:.5f}".format(usage_data["total_usage"] / 100)
            rounded_usage = round(usage_data["total_usage"] / 100, 5)
            usage_percent = round(usage_data["total_usage"] / usage_limit, 2)
            from ..webui import get_html

            # return i18n("**本月使用金额** ") + f"\u3000 ${rounded_usage}"
            return get_html("billing_info.html").format(
                label=i18n("本月使用金额"),
                usage_percent=usage_percent,
                rounded_usage=rounded_usage,
                usage_limit=usage_limit
            )
        except requests.exceptions.ConnectTimeout:
            status_text = (
                    STANDARD_ERROR_MSG + CONNECTION_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
            )
            return status_text
        except requests.exceptions.ReadTimeout:
            status_text = STANDARD_ERROR_MSG + READ_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
            return status_text
        except Exception as e:
            import traceback
            traceback.print_exc()
            logging.error(i18n("获取API使用情况失败:") + str(e))
            return STANDARD_ERROR_MSG + ERROR_RETRIEVE_MSG

    @shared.state.switching_api_key  # 在不开启多账号模式的时候，这个装饰器不会起作用
    def _get_response(self, stream=False):
        openai_api_key = self.api_key
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

        # 如果有自定义的api-host，使用自定义host发送请求，否则使用默认设置发送请求
        if shared.state.chat_completion_url != CHAT_COMPLETION_URL:
            logging.debug(f"使用自定义API URL: {shared.state.chat_completion_url}")

        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["HTTPS_PROXY"] = https_proxy
        with retrieve_proxy('http://127.0.0.1:7890'):
            try:
                response = requests.post(
                    shared.state.chat_completion_url,
                    headers=headers,
                    json=payload,
                    stream=stream,
                    timeout=timeout,
                )
            except:
                traceback.print_exc()
                return None
        return response

    def _refresh_header(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sensitive_id}",
        }

    def _get_billing_data(self, billing_url):
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["HTTPS_PROXY"] = https_proxy
        with retrieve_proxy('http://127.0.0.1:7890'):
            response = requests.get(
                billing_url,
                headers=self.headers,
                timeout=TIMEOUT_ALL,
            )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}: {response.text}"
            )

    def _decode_chat_response(self, response):
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

    def set_key(self, new_access_key):
        ret = super().set_key(new_access_key)
        self._refresh_header()
        return ret

    def _single_query_at_once(self, history, temperature=1.0):
        timeout = TIMEOUT_ALL
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "temperature": f"{temperature}",
        }
        payload = {
            "model": self.model_name,
            "messages": history,
        }
        # 如果有自定义的api-host，使用自定义host发送请求，否则使用默认设置发送请求
        if shared.state.chat_completion_url != CHAT_COMPLETION_URL:
            logging.debug(f"使用自定义API URL: {shared.state.chat_completion_url}")

        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["HTTPS_PROXY"] = https_proxy
        with retrieve_proxy('http://127.0.0.1:7890'):
            response = requests.post(
                shared.state.chat_completion_url,
                headers=headers,
                json=payload,
                stream=False,
                timeout=timeout,
            )

        return response

    def auto_name_chat_history(self, name_chat_method, user_question, chatbot, single_turn_checkbox):
        if len(self.history) == 2 and not single_turn_checkbox and not hide_history_when_not_logged_in:
            user_question = self.history[0]["content"]
            if name_chat_method == i18n("模型自动总结（消耗tokens）"):
                ai_answer = self.history[1]["content"]
                try:
                    history = [
                        {"role": "system", "content": SUMMARY_CHAT_SYSTEM_PROMPT},
                        {"role": "user",
                         "content": f"Please write a title based on the following conversation:\n---\nUser: {user_question}\nAssistant: {ai_answer}"}
                    ]
                    response = self._single_query_at_once(history, temperature=0.0)
                    response = json.loads(response.text)
                    content = response["choices"][0]["message"]["content"]
                    filename = replace_special_symbols(content) + ".json"
                except Exception as e:
                    logging.info(f"自动命名失败。{e}")
                    filename = replace_special_symbols(user_question)[:16] + ".json"
                return self.rename_chat_history(filename, chatbot)
            elif name_chat_method == i18n("第一条提问"):
                filename = replace_special_symbols(user_question)[:16] + ".json"
                return self.rename_chat_history(filename, chatbot)
            else:
                return gr.update()
        else:
            return gr.update()
