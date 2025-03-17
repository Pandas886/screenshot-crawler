# Screenshot Crawler

一个功能强大的网页截图和内容分析工具，支持网页截图、内容提取、多语言翻译和智能标签管理。

## 功能特点

- 网页截图：自动对指定URL进行高质量截图
- 内容分析：使用AI提取网页核心内容和关键信息
- 多语言支持：自动将内容翻译成指定语言
- 标签管理：智能分析和提取内容标签
- 简单易用：提供Web界面和API接口
- Docker支持：快速部署和扩展
## 安装和使用

直接使用
```angular2html
docker pull xxx.cloudeon.top/peterpoker/screenshot-crawler

docker run -d -p 7860:7860 --name screenshot xxx.cloudeon.top/peterpoker/screenshot-crawler
```

## 开发调试
必须安装依赖和字体
```
sudo apt-get update -y
sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libnss3 libnspr4


sudo mkdir /usr/share/fonts/chinese/
sudo cp weiruanyahei.ttf /usr/share/fonts/chinese/

```


## Docker构建和推送
构建命令：
docker build -t screenshot-crawler .

运行命令：
docker run -d -p 7860:7860 --name screenshot screenshot-crawler


推送docker：
docker tag screenshot-crawler peterpoker/screenshot-crawler
docker push peterpoker/screenshot-crawler
