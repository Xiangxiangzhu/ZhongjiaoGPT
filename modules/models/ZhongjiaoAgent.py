from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.docstore.document import Document
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from duckduckgo_search import DDGS
from itertools import islice

from typing import Any, Dict, List, Optional, Union

from langchain.callbacks.base import BaseCallbackHandler
from langchain.input import print_text
from langchain.schema import AgentAction, AgentFinish, LLMResult

from pydantic.v1 import BaseModel, Field

import requests
from bs4 import BeautifulSoup
from threading import Thread, Condition
from collections import deque

from .base_model import BaseLLMModel, CallbackToIterator, ChuanhuCallbackHandler
from ..config import default_chuanhu_assistant_model
from ..presets import SUMMARIZE_PROMPT, i18n
from ..index_func import construct_index

from langchain.callbacks import get_openai_callback
import os
import gradio as gr
import logging

PREFIX = """
[WHO ARE YOU]
你是一个专业的道路交通设计人员，擅长生成道路设计方案、立交桥设计方案等。

[YOUR ACTION GUILDLINES]
1.当你需要设计道路、立交桥时调用“生成立交方案”工具；
2.调用“生成立交方案”工具将在一个独立的设计软件RoadRunner中生成所需的设计方案；
3.在调用这个工具后你就已经完成了设计方案输出工作，仅仅高速用户这个工具的输出内容即可！
4.只输出最终答案！只输出最终答案！只输出最终答案！
"""

# FORMAT_INSTRUCTIONS = """请按照以下格式进行:
#
# 问题: 你需要回答的输入问题
# 思考: 你应该始终考虑接下来的行动
# 动作: 需要采取的行动，应该是以下选项之一[{tool_names}]
# 动作输入: 对行动的输入
# 观察: 行动的结果
# ...（这个思考/动作/动作输入/观察的过程可以重复N次）
# 思考: 我现在知道了最终的答案
# 最终答案: 对原始输入问题的最终回答"""

SUFFIX = """Begin!"

Question: {input}
{agent_scratchpad}"""


class DesignInput(BaseModel):
    keywords: str = Field(description="需要生成的对象")


class AgentClient(BaseLLMModel):
    def __init__(self, model_name, openai_api_key, user_name="") -> None:
        super().__init__(model_name=model_name, user=user_name)
        self.text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=30)
        self.api_key = openai_api_key
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model_name="gpt-3.5-turbo",
                              openai_api_base=os.environ.get("OPENAI_API_BASE", None))
        self.cheap_llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model_name="gpt-3.5-turbo",
                                    openai_api_base=os.environ.get("OPENAI_API_BASE", None))

        self.tools = []

        self.tools.append(
            Tool.from_function(
                func=self.gen_design,
                name="生成立交方案",
                description="用于生成立交桥尤其是全苜蓿叶形立交的设计方案",
                args_schema=DesignInput
            )
        )

        # self.tools.append(
        #     StructuredTool.from_function(
        #         func=self.ask_url,
        #         name="Ask Webpage",
        #         description="useful when you need to ask detailed questions about a webpage.",
        #         args_schema=WebAskingInput
        #     )
        # )

    def gen_design(self, element):
        a = self
        print("#################################")
        print("fafsadfjiosjfoijasjfoisj")
        print("#################################")
        result = "全苜蓿叶形立交桥设计方案已经生成，请在RoadRunner设计软件中进行查看！！！"
        return result

    def get_answer_at_once(self):
        question = self.history[-1]["content"]
        # llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                'prefix': PREFIX,
                # 'format_instructions': FORMAT_INSTRUCTIONS,
                'suffix': SUFFIX
            }
        )

        reply = agent.run(input=f"{question} Reply in 简体中文")
        return reply, -1

    def get_answer_stream_iter(self):
        question = self.history[-1]["content"]
        it = CallbackToIterator()
        manager = BaseCallbackManager(handlers=[ChuanhuCallbackHandler(it.callback)])

        def thread_func():

            agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                callback_manager=manager,
                agent_kwargs={
                    'prefix': PREFIX,
                    # 'format_instructions': FORMAT_INSTRUCTIONS,
                    'suffix': SUFFIX
                }
            )

            try:
                reply = agent.run(input=f"{question} Reply in 简体中文")
            except Exception as e:
                import traceback
                traceback.print_exc()
                reply = str(e)
            it.callback(reply)
            it.finish()

        t = Thread(target=thread_func)
        t.start()
        partial_text = ""
        for value in it:
            partial_text += value
            yield partial_text
