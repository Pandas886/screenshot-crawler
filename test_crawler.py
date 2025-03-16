import asyncio
from website_crawler import WebsitCrawler

async def main():
    # 创建爬虫实例
    crawler = WebsitCrawler()
    
    # 测试网站列表
    test_urls = [
        'www.baidu.com',
        'www.github.com',
        'www.python.org'
    ]
    
    try:
        # 依次测试每个网站
        for url in test_urls:
            # 添加重试机制
            max_retries = 3
            for retry in range(max_retries):
                try:
                    screenshot_path = await crawler.capture_screenshot(url)
                    if screenshot_path:
                        print(f'成功抓取 {url} 的截图，保存在: {screenshot_path}')
                        break
                    else:
                        print(f'抓取 {url} 失败，尝试 {retry+1}/{max_retries}')
                        if retry < max_retries - 1:
                            print(f'等待3秒后重试...')
                            await asyncio.sleep(3)
                except Exception as e:
                    print(f'抓取 {url} 出现异常: {e}，尝试 {retry+1}/{max_retries}')
                    if retry < max_retries - 1:
                        print(f'等待3秒后重试...')
                        await asyncio.sleep(3)
            else:
                print(f'抓取 {url} 失败，已达到最大重试次数 {max_retries}')
    finally:
        # 确保浏览器被关闭
        if crawler.browser:
            await crawler.browser.close()

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())