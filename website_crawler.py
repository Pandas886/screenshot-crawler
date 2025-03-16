import logging
import time
import random
import asyncio
import aiohttp
from pyppeteer import launch

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

global_agent_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

class WebsitCrawler:
    def __init__(self):
        self.browser = None

    # 确保浏览器实例存在并可用
    async def ensure_browser(self, retry_count=3):
        for attempt in range(retry_count):
            try:
                # 如果浏览器不存在或已关闭，创建新的浏览器实例
                if self.browser is None or not self.browser.process or self.browser.process.returncode is not None:
                    if self.browser:
                        try:
                            await self.browser.close()
                        except Exception:
                            pass  # 忽略关闭时的错误
                        self.browser = None
                    
                    logger.info(f"创建新的浏览器实例 (尝试 {attempt+1}/{retry_count})")
                    # 增加更多适用于Linux服务器环境的启动参数
                    self.browser = await launch(headless=True,
                                              ignoreDefaultArgs=["--enable-automation"],
                                              ignoreHTTPSErrors=True,
                                              args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
                                                    '--disable-software-rasterizer', '--disable-setuid-sandbox',
                                                    '--disable-extensions', '--no-zygote', '--single-process',
                                                    '--disable-accelerated-2d-canvas', '--disable-web-security',
                                                    '--disable-features=site-per-process', '--disable-breakpad'],
                                              handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                              executablePath=None,  # 允许系统自动查找Chromium路径
                                              env={'DISPLAY': ':0'})
                return True
            except Exception as e:
                logger.error(f"创建浏览器实例失败 (尝试 {attempt+1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    logger.info(f"等待2秒后重试...")
                    await asyncio.sleep(2)  # 等待一段时间后重试
                else:
                    logger.error(f"已达到最大重试次数 ({retry_count})，无法创建浏览器实例")
                    return False
        return False
            
    # 爬取指定URL网页并保存截图
    async def capture_screenshot(self, url):
        try:
            # 记录程序开始时间
            start_time = int(time.time())
            logger.info("正在处理：" + url)
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url

            # 确保浏览器实例存在并可用
            if not await self.ensure_browser():
                logger.error("无法创建浏览器实例，跳过处理")
                return None

            page = await self.browser.newPage()
            # 设置用户代理
            await page.setUserAgent(random.choice(global_agent_headers))

            # 设置页面视口大小并访问具体URL
            width = 1920  # 默认宽度为 1920
            height = 1080  # 默认高度为 1080
            await page.setViewport({'width': width, 'height': height})
            try:
                await page.goto(url, {'timeout': 60000, 'waitUntil': ['load', 'networkidle2']})
            except Exception as e:
                logger.info(f'页面加载超时,不影响继续执行后续流程:{e}')

            # 获取页面实际尺寸
            dimensions = await page.evaluate(f'''(width, height) => {{
                return {{
                    width: {width},
                    height: {height},
                    deviceScaleFactor: window.devicePixelRatio
                }};
            }}''', width, height)

            # 生成截图文件名并保存截图
            screenshot_path = './' + url.replace("https://", "").replace("http://", "").replace("/", "").replace(".", "-") + '.png'
            await page.screenshot({'path': screenshot_path, 'clip': {
                'x': 0,
                'y': 0,
                'width': dimensions['width'],
                'height': dimensions['height']
            }})

            logger.info(f"截图已保存到: {screenshot_path}")
            await page.close()
            # 上传截图到图床
            image_url = await self.upload_image(screenshot_path)
            if image_url:
                logger.info(f"图片已上传到图床，访问地址: {image_url}")
            return image_url

        except Exception as e:
            logger.error(f"处理{url}站点异常，错误信息: {e}")
            # 如果浏览器意外关闭，将browser设为None以便下次重新创建
            if "Browser closed unexpectedly" in str(e):
                self.browser = None
            return None
        finally:
            # 计算程序执行时间
            execution_time = int(time.time()) - start_time
            # 输出程序执行时间
            logger.info(f"处理{url}用时：{execution_time}秒")

    async def upload_image(self, image_path):
        """
        将图片上传到图床
        :param image_path: 本地图片路径
        :return: 上传成功返回图片URL，失败返回None
        """
        try:
            async with aiohttp.ClientSession() as session:
                with open(image_path, 'rb') as f:
                    data = aiohttp.FormData()
                    data.add_field('file', f, filename=image_path.split('\\')[-1])
                    data.add_field('permission', '1')

                    headers = {
                        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
                    }

                    async with session.post('https://image.dooo.ng/api/v1/upload',
                                          data=data,
                                          headers=headers) as response:
                        if response.status == 200:
                            json_data = await response.json()
                            if json_data.get('status'):
                                return json_data['data']['links']['url']
        except Exception as e:
            logger.error(f"图片上传失败: {e}")
        return None
