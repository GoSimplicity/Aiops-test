from ollama import Client, ResponseError
from config.settings import settings
from utils.helpers import parse_json_response
from utils.logger import logger


class OllamaModel:
    def __init__(self):
        logger.info("初始化 OllamaModel")
        self.client = Client(host=settings.ollama_api_url)
        self.model_name = settings.ollama_model_name
        logger.info(f"使用的模型名称: {self.model_name}")

    def get_intent(self, user_input: str) -> dict:
        """获取用户意图"""
        logger.info(f"发送用户输入到 Ollama: {user_input}")
        try:
            # 构建更严格的指令，要求模型只返回 JSON
            prompt = (
                f"你是一个 Kubernetes 管理助手。根据用户输入，返回一个严格的 JSON 对象，包含 'intent' 和 'parameters'。\n\n"
                f"用户输入: {user_input}\n"
                f"返回格式严格为：{{\"intent\": \"intent_name\", \"parameters\": {{...}}}}。其中 'intent' 使用英语，如 'list_pods'、'create_pod'、'delete_pod'。请勿添加其他文本或解释。"
            )

            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': prompt,
                    },
                ],
                format='json',
                stream=False
            )
            logger.debug(f"Ollama 原始响应: {response}")
            if 'message' in response and 'content' in response['message']:
                content = response['message']['content']
                logger.debug(f"Ollama 响应内容: {content}")
                parsed_response = parse_json_response(content)
                logger.debug(f"解析后的响应: {parsed_response}")
                return parsed_response
            else:
                logger.error("响应结构不符合预期")
                return {"error": "响应结构不符合预期"}
        except ResponseError as e:
            logger.error(f"Ollama API 错误: {e.error}, 状态码: {e.status_code}")
            return {"error": f"API 错误: {e.status_code}"}
        except Exception as e:
            logger.exception("调用 Ollama API 时发生异常")
            return {"error": str(e)}

    def list_models(self):
        """列出所有模型"""
        logger.info("请求列出所有模型")
        try:
            models = self.client.list()
            logger.info(f"获取到的模型列表: {models}")
            return models
        except Exception as e:
            logger.exception("获取模型列表时发生异常")
            return {"error": str(e)}
