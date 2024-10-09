import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from models.ollama_model import OllamaModel
from services.k8s_api import K8sAPIService
from models.intent_request import IntentRequest
from models.pod_manifest import PodManifest
from config.settings import settings
from utils.logger import logger

app = FastAPI()

logger.info(f"OLLAMA_API_URL: {settings.ollama_api_url}")
logger.info(f"OLLAMA_MODEL_NAME: {settings.ollama_model_name}")
logger.info(f"KUBERNETES_CONFIG_PATH: {settings.kube_config_path}")

# 创建服务实例作为全局依赖
ollama_model = OllamaModel()
k8s_api_service = K8sAPIService()


@app.post("/process/")
def process_command(request: IntentRequest):
    """
    处理用户命令，调用 Ollama 模型解析意图，并执行相应的 Kubernetes 操作。
    """
    user_input = request.user_input
    logger.info(f"用户输入: {user_input}")

    # 获取意图
    response = ollama_model.get_intent(user_input)
    logger.info(f"解析后的响应: {response}")

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    intent = response.get("intent")
    parameters = response.get("parameters", {})

    if not intent:
        raise HTTPException(status_code=400, detail="无法识别意图。")

    # 根据意图执行操作
    if intent == "list_pods":
        namespace = parameters.get("namespace", "default")
        result = k8s_api_service.list_pods(namespace)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    elif intent == "create_pod":
        namespace = parameters.get("namespace")
        pod_manifest = parameters.get("pod_manifest")
        if not namespace or not pod_manifest:
            raise HTTPException(status_code=400, detail="缺少必要的参数：namespace 或 pod_manifest。")
        result = k8s_api_service.create_pod(namespace, pod_manifest)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    elif intent == "delete_pod":
        namespace = parameters.get("namespace")
        pod_name = parameters.get("pod_name")
        if not namespace or not pod_name:
            raise HTTPException(status_code=400, detail="缺少必要的参数：namespace 或 pod_name。")
        result = k8s_api_service.delete_pod(namespace, pod_name)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    else:
        raise HTTPException(status_code=400, detail=f"未知的意图: {intent}")


@app.get("/list-models/")
def list_models(model: OllamaModel = Depends(lambda: ollama_model)):
    response = model.list_models()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response


@app.get("/list-pods/")
def list_pods(namespace: str = "default", k8s: K8sAPIService = Depends(lambda: k8s_api_service)):
    """列出指定命名空间中的所有Pod"""
    result = k8s.list_pods(namespace)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.post("/create-pod/")
def create_pod(namespace: str, pod_manifest: PodManifest, k8s: K8sAPIService = Depends(lambda: k8s_api_service)):
    """在指定命名空间中创建Pod"""
    result = k8s.create_pod(namespace, pod_manifest.dict())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.on_event("shutdown")
def shutdown_event():
    logger.info("应用关闭")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9999, reload=True)
