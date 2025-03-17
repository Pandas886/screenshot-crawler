import asyncio
from website_crawler import WebsitCrawler

async def main():
    # 创建爬虫实例
    crawler = WebsitCrawler()
    
    # 测试URL
    test_url = 'https://github.com/Dataherald/dataherald'
    
    # 测试标签和语言
    test_tags = ['technology', 'development', 'git']
    test_languages = ['en', 'zh', 'ja']
    
    try:
        # 添加重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                result = await crawler.capture_screenshot(test_url, tags=test_tags, languages=test_languages)
                if result:
                    print(f'成功抓取 {test_url} 的数据：')
                    print(f'- 标题: {result["title"]}')
                    print(f'- 描述: {result["description"]}')
                    print(f'- 截图URL: {result["screenshot_data"]}')
                    if result['tags']:
                        print(f'- 标签: {result["tags"]}')
                    if result['languages']:
                        print('- 多语言内容:')
                        for lang in result['languages']:
                            print(f'  {lang["language"]}:')
                            print(f'    标题: {lang["title"]}')
                            print(f'    描述: {lang["description"]}')
                    break
                else:
                    print(f'抓取 {test_url} 失败，尝试 {retry+1}/{max_retries}')
                    if retry < max_retries - 1:
                        print(f'等待3秒后重试...')
                        await asyncio.sleep(3)
            except Exception as e:
                print(f'抓取 {test_url} 出现异常: {e}，尝试 {retry+1}/{max_retries}')
                if retry < max_retries - 1:
                    print(f'等待3秒后重试...')
                    await asyncio.sleep(3)
        else:
            print(f'抓取 {test_url} 失败，已达到最大重试次数 {max_retries}')
    finally:
        # 确保浏览器被关闭
        if crawler.browser:
            await crawler.browser.close()

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())