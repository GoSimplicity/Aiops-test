import json
from typing import Union, Dict

from utils.logger import logger


def parse_json_response(response_content: Union[str, Dict]) -> Dict:
    """
    解析 Ollama 响应。
    如果输入是字符串，尝试解析为 JSON。
    如果输入已经是字典，直接返回。
    """
    if isinstance(response_content, dict):
        return response_content
    elif isinstance(response_content, str):
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            logger.warning("JSON 解析失败，返回原始响应")
            return {"response": response_content}
    else:
        return {"error": "未知的响应格式"}
