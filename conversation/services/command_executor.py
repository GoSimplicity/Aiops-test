from services.k8s_api import K8sAPIService
from utils.logger import logger


class CommandExecutorService:
    def __init__(self):
        self.k8s_service = K8sAPIService()

    async def execute_command(self, command: dict) -> dict:
        """执行解析后的指令"""
        logger.info(f"执行指令: {command}")
        command_type = command.get("type")
        if command_type == "list_pods":
            namespace = command.get("namespace", "default")
            return self.k8s_service.list_pods(namespace)
        elif command_type == "create_pod":
            namespace = command.get("namespace", "default")
            pod_manifest = command.get("pod_manifest", {})
            return self.k8s_service.create_pod(namespace, pod_manifest)
        else:
            logger.error(f"未知的指令类型: {command_type}")
            return {"error": f"未知的指令类型: {command_type}"}
