# 使用自己的 Miniconda 镜像
FROM christtzm/tzm_dev:conda 

# 设置 Zsh 为默认 Shell
SHELL ["/usr/bin/zsh", "-c"]

# 安装开发组件及conda环境
RUN /root/miniconda3/bin/conda create -n zhongjiao python=3.9 -y

# RUN apt-get update \
#     && apt-get install -y build-essential \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
# 	&& /root/miniconda3/bin/conda create -n zhongjiao python=3.9 -y

# 配置环境变量，简化之后的命令
ENV PATH="/root/miniconda3/envs/zhongjiao/bin:$PATH" \
    CONDA_DEFAULT_ENV="zhongjiao" \
    dockerrun="yes"

# 拷贝 Python 依赖文件并安装
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 拷贝应用代码
COPY . /app
WORKDIR /app

RUN chmod +x /app/add_semantic_router.sh && \
    ./add_semantic_router.sh

# CMD 指令
CMD ["python3", "-u", "ZhongjiaoChatbot.py", "2>&1", "|", "tee", "/var/log/application.log"]

# 暴露端口
EXPOSE 7860

