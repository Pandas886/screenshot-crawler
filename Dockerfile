# 阶段1: 构建应用程序
FROM python:3.10 AS builder

# 1.1 复制必要文件
WORKDIR /app
COPY requirements.txt /app/
COPY weiruanyahei.ttf /app/
COPY *.py /app/

# 1.2 安装python依赖
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --target=/app/dependencies -r requirements.txt

# 阶段2: 创建轻量级的运行时镜像
FROM python:3.10-slim

# 2.1 复制字体，避免乱码
WORKDIR /usr/share/fonts/chinese/
COPY --from=builder /app/weiruanyahei.ttf /usr/share/fonts/chinese/

# 2.2 复制执行所需的文件
COPY --from=builder /app/dependencies /app/dependencies
COPY --from=builder /app/*.py /app/

# 2.3 安装系统依赖
RUN apt-get update -y && \
    apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 \
    libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 libnss3 libnspr4 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2.4 设置 PYTHONPATH 环境变量
ENV PYTHONPATH=/app/dependencies

# 2.5 暴露端口
EXPOSE 7860

# 2.6 运行Gradio应用
CMD ["python", "gradio_app.py"]