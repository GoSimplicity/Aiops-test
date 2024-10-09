from models.ollama_model import OllamaModel
from utils.logger import logger


class IntentRecognitionService:
    def __init__(self):
        self.model = OllamaModel()

    def recognize_intent(self, user_input: str) -> dict:
        """识别用户意图"""
        logger.info(f"识别用户输入的意图: {user_input}")
        response = self.model.get_intent(user_input)
        if "error" in response:
            logger.error(f"意图识别失败: {response['error']}")
        else:
            logger.info(f"识别到的意图: {response}")
        return response
