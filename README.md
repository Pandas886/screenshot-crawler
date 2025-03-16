必须安装依赖和字体
```
sudo apt-get update -y
sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libnss3 libnspr4


sudo mkdir /usr/share/fonts/chinese/
sudo cp weiruanyahei.ttf /usr/share/fonts/chinese/

```



构建命令：
docker build -t tap4-ai-crawler .

运行命令：
docker run -d -p 7860:7860 --name tap4-ai-crawler tap4-ai-crawler