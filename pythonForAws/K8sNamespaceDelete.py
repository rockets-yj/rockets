from kubernetes import client, config

def delete_kubernetes_namespace(namespace_name):
    # 현재 클러스터의 kubeconfig 파일 로드
    config.load_kube_config()

    # 삭제할 네임스페이스 지정
    body = client.V1DeleteOptions()
    
    # Kubernetes API 인스턴스 생성
    api_instance = client.CoreV1Api()

    # 네임스페이스 삭제 요청
    try:
        api_instance.delete_namespace(name=namespace_name, body=body)
    
    except Exception as e:
        return e




# 함수 호출

if __name__ == '__main__':
    delete_kubernetes_namespace('test1')
    
    
    
    