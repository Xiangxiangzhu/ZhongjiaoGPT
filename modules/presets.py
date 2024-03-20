# -*- coding:utf-8 -*-
import os
from pathlib import Path
import gradio as gr
from .webui_locale import I18nAuto

i18n = I18nAuto()  # internationalization

CHATGLM_MODEL = None
CHATGLM_TOKENIZER = None
LLAMA_MODEL = None
LLAMA_INFERENCER = None
GEMMA_MODEL = None
GEMMA_TOKENIZER = None

# ChatGPT 设置
INITIAL_SYSTEM_PROMPT = "You are a helpful assistant."
API_HOST = "api.openai.com"
OPENAI_API_BASE = "https://api.openai.com/v1"
CHAT_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
IMAGES_COMPLETION_URL = "https://api.openai.com/v1/images/generations"
COMPLETION_URL = "https://api.openai.com/v1/completions"
BALANCE_API_URL = "https://api.openai.com/dashboard/billing/credit_grants"
USAGE_API_URL = "https://api.openai.com/dashboard/billing/usage"
HISTORY_DIR = Path("history")
# HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

# 错误信息
STANDARD_ERROR_MSG = i18n("☹️发生了错误：")  # 错误信息的标准前缀
GENERAL_ERROR_MSG = i18n("获取对话时发生错误，请查看后台日志")
ERROR_RETRIEVE_MSG = i18n("请检查网络连接，或者API-Key是否有效。")
CONNECTION_TIMEOUT_MSG = i18n("连接超时，无法获取对话。")  # 连接超时
READ_TIMEOUT_MSG = i18n("读取超时，无法获取对话。")  # 读取超时
PROXY_ERROR_MSG = i18n("代理错误，无法获取对话。")  # 代理错误
SSL_ERROR_PROMPT = i18n("SSL错误，无法获取对话。")  # SSL 错误
NO_APIKEY_MSG = i18n("API key为空，请检查是否输入正确。")  # API key 长度不足 51 位
NO_INPUT_MSG = i18n("请输入对话内容。")  # 未输入对话内容
BILLING_NOT_APPLICABLE_MSG = i18n("账单信息不适用")  # 本地运行的模型返回的账单信息

TIMEOUT_STREAMING = 60  # 流式对话时的超时时间
TIMEOUT_ALL = 200  # 非流式对话时的超时时间
ENABLE_STREAMING_OPTION = True  # 是否启用选择选择是否实时显示回答的勾选框
ENABLE_LLM_NAME_CHAT_OPTION = True  # 是否启用选择是否使用LLM模型的勾选框
CONCURRENT_COUNT = 100  # 允许同时使用的用户数量

SIM_K = 5
INDEX_QUERY_TEMPRATURE = 1.0

CHUANHU_TITLE = i18n("中交GPT")

CHUANHU_DESCRIPTION = i18n(
    "由中交一公院 马小龙 孙铸 田赵明 研发<br />访问中交GPT的 [GitHub项目](https://github.com/) 下载最新版脚本")

ONLINE_MODELS = [
    "GPT3.5 Turbo",
    # "GPT3.5 Turbo Instruct",
    # "GPT3.5 Turbo 16K",
    # "GPT3.5 Turbo 0301",
    # "GPT3.5 Turbo 0613",
    # "GPT3.5 Turbo 1106",
    "GPT4",
    # "GPT4 32K",
    # "GPT4 Turbo",
    # "GPT4 Vision",
    # "川虎助理",
    # "川虎助理 Pro",
    # "DALL-E 3",
    # "Gemini Pro",
    # "Gemini Pro Vision",
    # "GooglePaLM",
    # "Gemma 2B",
    # "Gemma 7B",
    # "xmchat",
    # "Azure OpenAI",
    # "yuanai-1.0-base_10B",
    # "yuanai-1.0-translate",
    # "yuanai-1.0-dialog",
    # "yuanai-1.0-rhythm_poems",
    # "minimax-abab5-chat",
    # "midjourney",
    # "讯飞星火大模型V3.0",
    # "讯飞星火大模型V2.0",
    # "讯飞星火大模型V1.5",
    # "Claude 3 Sonnet",
    # "Claude 3 Opus",
    # "ERNIE-Bot-turbo",
    # "ERNIE-Bot",
    # "ERNIE-Bot-4",
    # "Ollama"
]

LOCAL_MODELS = [
    "Qwen1.5-72B",
    "Qwen1.5-14B",
    "Qwen1.5-7B",
    "Yi-34B",
    "Yi-6B",
    "Mistral-7B",
    "Llama2-70B",
    "Llama2-13B",
    "Llama2-7B",
    "chatglm3-6b",
    # "Baichuan2-13B",
    # "Baichuan2-7B"
    # "chatglm-6b",
    # "chatglm-6b-int4",
    # "chatglm-6b-int4-ge",
    # "chatglm2-6b",
    # "chatglm2-6b-int4",
    # "chatglm3-6b",
    # "chatglm3-6b-32k",
    # "StableLM",
    # "MOSS",
]

# Additional metadata for online and local models
MODEL_METADATA = {
    # "Llama-2-7B": {
    #     "repo_id": "TheBloke/Llama-2-7B-GGUF",
    #     "filelist": ["llama-2-7b.Q6_K.gguf"],
    # },
    # "Llama-2-7B-Chat": {
    #     "repo_id": "TheBloke/Llama-2-7b-Chat-GGUF",
    #     "filelist": ["llama-2-7b-chat.Q6_K.gguf"],
    # },
    # "Qwen 7B": {
    #     "repo_id": "Qwen/Qwen-7B-Chat-Int4",
    # },
    # "Qwen 14B": {
    #     "repo_id": "Qwen/Qwen-14B-Chat-Int4",
    # },

    "Qwen1.5-72B": {
        "repo_id": "",
    },
    "Qwen1.5-14B": {
        "repo_id": "",
    },
    "Qwen1.5-7B": {
        "repo_id": "",
    },
    "Yi-34B": {
        "repo_id": "",
    },
    "Yi-6B": {
        "repo_id": "",
    },
    "Mistral-7B": {
        "repo_id": "",
    },
    "Llama2-70B": {
        "repo_id": "",
    },
    "Llama2-13B": {
        "repo_id": "",
    },
    "Llama2-7B": {
        "repo_id": "",
    },
    "chatglm3-6b": {
        "repo_id": "",
    },

    "GPT3.5 Turbo": {
        "model_name": "gpt-3.5-turbo",
        "token_limit": 4096,
    },
    # "GPT3.5 Turbo Instruct": {
    #     "model_name": "gpt-3.5-turbo-instruct",
    #     "token_limit": 4096,
    # },
    # "GPT3.5 Turbo 16K": {
    #     "model_name": "gpt-3.5-turbo-16k",
    #     "token_limit": 16384,
    # },
    # "GPT3.5 Turbo 0301": {
    #     "model_name": "gpt-3.5-turbo-0301",
    #     "token_limit": 4096,
    # },
    # "GPT3.5 Turbo 0613": {
    #     "model_name": "gpt-3.5-turbo-0613",
    #     "token_limit": 4096,
    # },
    # "GPT3.5 Turbo 1106": {
    #     "model_name": "gpt-3.5-turbo-1106",
    #     "token_limit": 16384,
    # },
    "GPT4": {
        "model_name": "gpt-4",
        "token_limit": 8192,
    },
    # "GPT4 32K": {
    #     "model_name": "gpt-4-32k",
    #     "token_limit": 32768,
    # },
    # "GPT4 Turbo": {
    #     "model_name": "gpt-4-turbo-preview",
    #     "token_limit": 128000,
    # },
    # "GPT4 Vision": {
    #     "model_name": "gpt-4-vision-preview",
    #     "token_limit": 128000,
    #     "multimodal": True
    # },
    # "Claude": {
    #     "model_name": "Claude",
    #     "token_limit": 4096,
    # },
    # "Claude 3 Sonnet": {
    #     "model_name": "claude-3-sonnet-20240229",
    #     "token_limit": 200000,
    #     "max_generation": 4096,
    #     "multimodal": True
    # },
    # "Claude 3 Opus": {
    #     "model_name": "claude-3-opus-20240229",
    #     "token_limit": 200000,
    #     "max_generation": 4096,
    #     "multimodal": True
    # },
    # "ERNIE-Bot-turbo": {
    #     "model_name": "ERNIE-Bot-turbo",
    #     "token_limit": 1024,
    # },
    # "ERNIE-Bot": {
    #     "model_name": "ERNIE-Bot",
    #     "token_limit": 1024,
    # },
    # "ERNIE-Bot-4": {
    #     "model_name": "ERNIE-Bot-4",
    #     "token_limit": 1024,
    # },
    # "Gemini Pro": {
    #     "model_name": "gemini-pro",
    #     "token_limit": 30720,
    # },
    # "Gemini Pro Vision": {
    #     "model_name": "gemini-pro-vision",
    #     "token_limit": 30720,
    # },
    # "Ollama": {
    #     "model_name": "ollama",
    #     "token_limit": 4096,
    # },
    # "Gemma 2B": {
    #     "repo_id": "google/gemma-2b-it",
    #     "model_name": "gemma-2b-it",
    #     "token_limit": 8192,
    # },
    # "Gemma 7B": {
    #     "repo_id": "google/gemma-7b-it",
    #     "model_name": "gemma-7b-it",
    #     "token_limit": 8192,
    # }
}

if os.environ.get('HIDE_LOCAL_MODELS', 'false') == 'true':
    MODELS = ONLINE_MODELS
else:
    MODELS = ONLINE_MODELS + LOCAL_MODELS

DEFAULT_MODEL = 0

os.makedirs("models", exist_ok=True)
os.makedirs("lora", exist_ok=True)
os.makedirs("history", exist_ok=True)
for dir_name in os.listdir("models"):
    if os.path.isdir(os.path.join("models", dir_name)):
        display_name = None
        for model_name, metadata in MODEL_METADATA.items():
            if "model_name" in metadata and metadata["model_name"] == dir_name:
                display_name = model_name
                break
        if display_name is None:
            MODELS.append(dir_name)

TOKEN_OFFSET = 1000  # 模型的token上限减去这个值，得到软上限。到达软上限之后，自动尝试减少token占用。
DEFAULT_TOKEN_LIMIT = 3000  # 默认的token上限
REDUCE_TOKEN_FACTOR = 0.5  # 与模型token上限想乘，得到目标token数。减少token占用时，将token占用减少到目标token数以下。

REPLY_LANGUAGES = [
    "简体中文",
    "繁體中文",
    "English",
    "日本語",
    "Español",
    "Français",
    "Russian",
    "Deutsch",
    "한국어",
    "跟随问题语言（不稳定）"
]

HISTORY_NAME_METHODS = [
    i18n("根据日期时间"),
    i18n("第一条提问"),
    i18n("模型自动总结（消耗tokens）"),
]

DIRECTLY_SUPPORTED_IMAGE_FORMATS = (
    ".png", ".jpeg", ".gif",
    ".webp")  # image types that can be directly uploaded, other formats will be converted to jpeg
IMAGE_FORMATS = DIRECTLY_SUPPORTED_IMAGE_FORMATS + (".jpg", ".bmp", "heic", "heif")  # all supported image formats

WEBSEARCH_PTOMPT_TEMPLATE = """\
Web search results:

{web_results}
Current date: {current_date}

Instructions: Using the provided web search results, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.
Query: {query}
Reply in {reply_language}
"""

PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Current date: {current_date}.
Using the provided context information, write a comprehensive reply to the given query.
Make sure to cite results using [number] notation after the reference.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject.
Use prior knowledge only if the given context didn't provide enough information.
Answer the question: {query_str}
Reply in {reply_language}
"""

REFINE_TEMPLATE = """\
The original question is as follows: {query_str}
We have provided an existing answer: {existing_answer}
We have the opportunity to refine the existing answer
(only if needed) with some more context below.
------------
{context_msg}
------------
Given the new context, refine the original answer to better
Reply in {reply_language}
If the context isn't useful, return the original answer.
"""

SUMMARIZE_PROMPT = """Write a concise summary of the following:

{text}

CONCISE SUMMARY IN 中文:"""

SUMMARY_CHAT_SYSTEM_PROMPT = """\
Please summarize the following conversation for a chat topic.
No more than 16 characters.
No special characters.
Punctuation mark is banned.
Not including '.' ':' '?' '!' '“' '*' '<' '>'.
Reply in user's language.
"""

ALREADY_CONVERTED_MARK = "<!-- ALREADY CONVERTED BY PARSER. -->"
START_OF_OUTPUT_MARK = "<!-- SOO IN MESSAGE -->"
END_OF_OUTPUT_MARK = "<!-- EOO IN MESSAGE -->"

small_and_beautiful_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#EBFAF2",
        c100="#CFF3E1",
        c200="#A8EAC8",
        c300="#77DEA9",
        c400="#3FD086",
        c500="#02C160",
        # c600="#06AE56",
        c600="#00BFFF",
        c700="#05974E",
        c800="#057F45",
        c900="#04673D",
        c950="#2E5541",
        name="small_and_beautiful",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#E3F0F7",
        c200="#7EBCE2",
        c300="#00BFFF",
        c400="#576b95",
        c500="#5F9EA0",
        c600="#7B68EE",
        c700="#576b95",
        c800="#576b95",
        c900="#5F9EA0",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f6f7f8",
        # c100="#f3f4f6",
        c100="#F2F2F2",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        # c900="#272727",
        c900="#2B2B2B",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    # # button_primary_background_fill="*primary_500",
    # button_primary_background_fill_dark="*primary_600",
    # # button_primary_background_fill_hover="*primary_400",
    # # button_primary_border_color="*primary_500",
    # button_primary_border_color_dark="*primary_600",
    # button_primary_text_color="white",
    # button_primary_text_color_dark="white",
    # button_secondary_background_fill="*neutral_100",
    # button_secondary_background_fill_hover="*neutral_50",
    # button_secondary_background_fill_dark="*neutral_900",
    # button_secondary_text_color="*neutral_800",
    # button_secondary_text_color_dark="white",
    # # background_fill_primary="#F7F7F7",
    # # background_fill_primary_dark="#1F1F1F",
    # # block_title_text_color="*primary_500",
    # block_title_background_fill_dark="*primary_900",
    # block_label_background_fill_dark="*primary_900",
    # input_background_fill="#F6F6F6",
    # # chatbot_code_background_color="*neutral_950",
    # # gradio 会把这个几个chatbot打头的变量应用到其他md渲染的地方，鬼晓得怎么想的。。。
    # chatbot_code_background_color_dark="*neutral_950",

    # 颜色方案2

    color_accent="*secondary_300",

    block_title_background_fill="*secondary_100",
    block_title_text_color="*secondary_200",
    block_label_text_color="*secondary_200",
    block_label_background_fill="*secondary_100",
    button_primary_background_fill="*secondary_100",

    button_primary_background_fill_hover="*secondary_200",
    button_primary_background_fill_hover_dark="*secondary_900",
    button_primary_text_color_hover="white",
    button_primary_text_color_hover_dark="white",

    button_primary_background_fill_dark="*secondary_900",
    button_primary_border_color_dark="*secondary_900",
    button_primary_text_color="*secondary_200",
    button_primary_text_color_dark="white",
    button_secondary_background_fill="*neutral_100",
    button_secondary_background_fill_hover="*secondary_100",
    button_secondary_background_fill_hover_dark="*secondary_900",
    button_secondary_background_fill_dark="*neutral_900",
    button_secondary_text_color="*neutral_800",
    button_secondary_text_color_dark="white",
    block_title_background_fill_dark="*secondary_900",
    block_label_background_fill_dark="*secondary_900",
    input_background_fill="#F6F6F6",
    chatbot_code_background_color_dark="*neutral_950",
)
