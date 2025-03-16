from gradio_client import Client

client = Client("https://7860-6677ai-tap4aicrawler-ydzvaj4zffw.ws-us118.gitpod.io/")
result = client.predict(
		url="https://github.com/6677-ai/tap4-ai-crawler",
		api_name="/process_url"
)
print(result)