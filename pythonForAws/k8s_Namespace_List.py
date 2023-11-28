from kubernetes import client,config

def load_kubernetes_namespace():
    # 현재 실행 중인 클러스터의 kubeconfig 로드
    config.load_kube_config()
    
    # Kunbernetes API 서버에서 namespace 목록 가져오기
    api_instance = client.CoreV1Api()
    namespaces = api_instance.list_namespace()
    
    # 가져온 namespace 출력   
    print("namespace 목록 : ")
    for ns in namespaces.items:
        print(f"- {ns.metadata.name}")
        # if ns.metadata.name == "default":
        #     print("default namespace!")
        #     break

if __name__=="__main__":
    load_kubernetes_namespace()