from kubernetes import client, config
from utils.logger import logger
from config.settings import settings


class K8sAPIService:
    def __init__(self):
        config_path = settings.kube_config_path
        try:
            config.load_kube_config(config_path)
            logger.info(f"成功加载Kubernetes配置文件: {config_path}")
        except Exception as e:
            logger.exception(f"加载Kubernetes配置文件失败: {e}")
            raise e
        self.v1 = client.CoreV1Api()

    def list_pods(self, namespace: str = "default"):
        """列出指定命名空间中的所有Pod"""
        try:
            pods = self.v1.list_namespaced_pod(namespace)
            pod_names = [pod.metadata.name for pod in pods.items]
            logger.info(f"获取到的Pod列表: {pod_names}")
            logger.debug(f"完整的Pod信息: {pods.to_dict()}")
            return {"pods": pod_names}
        except Exception as e:
            logger.exception("列出Pod时发生异常")
            return {"error": str(e)}

    def create_pod(self, namespace: str, pod_manifest: dict):
        """在指定命名空间中创建Pod"""
        try:
            self.v1.create_namespaced_pod(namespace, pod_manifest)
            logger.info(f"在命名空间 {namespace} 中创建Pod成功")
            return {"status": "Pod创建成功"}
        except Exception as e:
            logger.exception("创建Pod时发生异常")
            return {"error": str(e)}

    def delete_pod(self, namespace: str, pod_name: str):
        """在指定命名空间中删除Pod"""
        try:
            self.v1.delete_namespaced_pod(pod_name, namespace)
            logger.info(f"在命名空间 {namespace} 中删除Pod {pod_name} 成功")
            return {"status": f"Pod {pod_name} 删除成功"}
        except Exception as e:
            logger.exception("删除Pod时发生异常")
            return {"error": str(e)}