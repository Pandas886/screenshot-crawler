import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
from common_util import CommonUtil

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
util = CommonUtil()

class LLMUtil:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL')
        logger.info(f"OpenAI Base URL:{self.openai_base_url}")
        self.detail_sys_prompt = os.getenv('DETAIL_SYS_PROMPT')
        self.tag_selector_sys_prompt = os.getenv('TAG_SELECTOR_SYS_PROMPT')
        self.language_sys_prompt = os.getenv('LANGUAGE_SYS_PROMPT')
        self.openai_model = os.getenv('OPENAI_MODEL')
        self.openai_max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', 5000))
        self.client = OpenAI(
            api_key=self.openai_api_key,
            base_url=self.openai_base_url
        )

    def process_detail(self, user_prompt):
        logger.info("正在处理Detail...")
        return util.detail_handle(self.process_prompt(self.detail_sys_prompt, user_prompt))

    def process_tags(self, user_prompt):
        logger.info(f"正在处理tags...")
        result = self.process_prompt(self.tag_selector_sys_prompt, user_prompt)
        # 将result（逗号分割的字符串）转为数组
        if result:
            tags = [element.strip() for element in result.split(',')]
        else:
            tags = []
        logger.info(f"tags处理结果:{tags}")
        return tags

    def process_language(self, language, user_prompt):
        logger.info(f"正在处理多语言:{language}, user_prompt:{user_prompt}")
        # 如果language 包含 English字符，则直接返回
        if 'english'.lower() in language.lower():
            result = user_prompt
        else:
            result = self.process_prompt(self.language_sys_prompt.replace("{language}", language), user_prompt)
            if result and not user_prompt.startswith("#"):
                # 如果原始输入没有包含###开头的markdown标记，则去掉markdown标记
                result = result.replace("### ", "").replace("## ", "").replace("# ", "").replace("**", "")
        logger.info(f"多语言:{language}, 处理结果:{result}")
        return result

    def process_prompt(self, sys_prompt, user_prompt):
        if not sys_prompt:
            logger.info(f"LLM无需处理，sys_prompt为空:{sys_prompt}")
            return None
        if not user_prompt:
            logger.info(f"LLM无需处理，user_prompt为空:{user_prompt}")
            return None

        logger.info("LLM正在处理")
        try:
            if len(user_prompt) > self.openai_max_tokens:
                logger.info(f"用户输入长度超过{self.openai_max_tokens}，进行截取")
                user_prompt = user_prompt[:self.openai_max_tokens]

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": sys_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.openai_model,
                temperature=0.2,
            )
            if chat_completion.choices[0] and chat_completion.choices[0].message:
                logger.info(f"LLM完成处理，成功响应!")
                return chat_completion.choices[0].message.content
            else:
                logger.info("LLM完成处理，处理结果为空")
                return None
        except Exception as e:
            logger.error(f"LLM处理失败", e)
            return None