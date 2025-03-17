FROM gitpod/workspace-full

RUN sudo apt-get update -y && \
    sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 \
    libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 libnss3 libnspr4 && \
    sudo rm -rf /var/lib/apt/lists/*

# 创建字体目录并复制字体文件
RUN sudo mkdir -p /usr/share/fonts/chinese/
COPY weiruanyahei.ttf /usr/share/fonts/chinese/

# 设置Python环境
RUN pyenv install 3.10 && \
    pyenv global 3.10