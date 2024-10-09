import logging

# 创建日志记录器
logger = logging.getLogger("ollama_logger")
logger.setLevel(logging.DEBUG)  # 设置为 DEBUG 以捕获更多信息

# 创建控制台处理器并设置日志级别
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(ch)