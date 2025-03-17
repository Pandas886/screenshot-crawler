import gradio as gr
import asyncio
from website_crawler import WebsitCrawler

# 创建爬虫实例
crawler = WebsitCrawler()

async def capture_and_upload(url, tags=None, languages=None):
    """处理URL输入，进行截图并上传"""
    try:
        # 添加重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                result = await crawler.capture_screenshot(url, tags, languages)
                if result:
                    # 返回所有爬取结果
                    return (
                        result.get('name', ''),
                        result.get('url', ''),
                        result.get('title', ''),
                        result.get('description', ''),
                        result.get('detail', ''),
                        result.get('screenshot_data', ''),
                        result.get('screenshot_thumbnail_data', ''),
                        str(result.get('tags', [])),
                        str(result.get('languages', []))
                    )
                else:
                    if retry < max_retries - 1:
                        await asyncio.sleep(3)
                    continue
            except Exception as e:
                if retry < max_retries - 1:
                    await asyncio.sleep(3)
                continue
        return None, None, None, None, None, None, None, None, None
    except Exception as e:
        return None, None, None, None, None, None, None, None, None
    finally:
        # 确保在发生异常时浏览器被正确关闭
        if crawler.browser:
            await crawler.browser.close()

def process_url(url, tags, languages):
    """同步包装异步函数"""
    # 处理标签输入
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
    # 处理语言输入
    language_list = languages if languages else []
    return asyncio.run(capture_and_upload(url, tag_list, language_list))

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("## 网站信息爬取工具")
    
    with gr.Row():
        with gr.Column(scale=4):
            url_input = gr.Textbox(
                label="输入网站URL",
                placeholder="请输入要爬取的网站URL（例如：www.example.com）"
            )
            tags_input = gr.Textbox(
                label="输入标签",
                placeholder="请输入标签，多个标签用逗号分隔（例如：技术,博客,开源）",
                value="技术,美食"
            )
            languages_input = gr.Dropdown(
                label="选择语言",
                choices=["en", "zh", "ja", "ko", "fr", "de", "es", "ru"],
                multiselect=True,
                value=["zh"]
            )
        with gr.Column(scale=1):
            submit_btn = gr.Button("开始爬取", variant="primary")
    
    with gr.Tabs():
        with gr.TabItem("基本信息"):
            with gr.Row():
                with gr.Column():
                    name_output = gr.Textbox(label="网站名称", interactive=False)
                    url_output = gr.Textbox(label="网站URL", interactive=False)
                    title_output = gr.Textbox(label="网站标题", interactive=False)
                    description_output = gr.Textbox(
                        label="网站描述",
                        interactive=False,
                        lines=3
                    )
        
        with gr.TabItem("详细内容"):
            detail_output = gr.Markdown(label="详细内容")
        
        with gr.TabItem("标签与多语言"):
            with gr.Row():
                tags_output = gr.Textbox(
                    label="标签",
                    interactive=False,
                    lines=2
                )
            with gr.Row():
                languages_output = gr.Textbox(
                    label="多语言内容",
                    interactive=False,
                    lines=5
                )
        
        with gr.TabItem("网站截图"):
            with gr.Row():
                image_url_output = gr.Textbox(label="图片URL", interactive=False)
            with gr.Row():
                image_output = gr.Image(label="截图预览")
    
    # 绑定提交按钮事件
    submit_btn.click(
        fn=process_url,
        inputs=[url_input, tags_input, languages_input],
        outputs=[
            name_output,
            url_output,
            title_output,
            description_output,
            detail_output,
            image_url_output,
            image_output,
            tags_output,
            languages_output
        ]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", share=True)