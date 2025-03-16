import gradio as gr
import asyncio
from website_crawler import WebsitCrawler

# 创建爬虫实例
crawler = WebsitCrawler()

async def capture_and_upload(url):
    """处理URL输入，进行截图并上传"""
    try:
        # 添加重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                image_url = await crawler.capture_screenshot(url)
                if image_url:
                    # 直接返回远程图片URL用于显示
                    return image_url, gr.update(value=image_url)
                else:
                    if retry < max_retries - 1:
                        await asyncio.sleep(3)
                    continue
            except Exception as e:
                if retry < max_retries - 1:
                    await asyncio.sleep(3)
                continue
        return None, None
    except Exception as e:
        return None, None
    finally:
        # 确保在发生异常时浏览器被正确关闭
        if crawler.browser:
            await crawler.browser.close()

def process_url(url):
    """同步包装异步函数"""
    return asyncio.run(capture_and_upload(url))

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("## 网站截图工具")
    with gr.Row():
        url_input = gr.Textbox(label="输入网站URL", placeholder="请输入要截图的网站URL（例如：www.example.com）")
    with gr.Row():
        submit_btn = gr.Button("开始截图")
    with gr.Row():
        text_output = gr.Textbox(label="图片URL", show_label=True)
    with gr.Row():
        image_output = gr.Image(label="截图预览", show_label=True)
    
    # 绑定提交按钮事件
    submit_btn.click(
        fn=process_url,
        inputs=[url_input],
        outputs=[text_output, image_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)