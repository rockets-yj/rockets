from kubernetes import client,config

# 생성할 namespace 의 이름을 받아와서 그 이름으로 namespace 생성
def create_kubernetes_namespace(namespace_name):
    # 현재 실행 중인 클러스터의 kubeconfig 로드
    config.load_kube_config()
    
    # Kunbernetes API 서버에서 namespace 목록 가져오기
    api_instance = client.CoreV1Api()
    namespaces = api_instance.list_namespace()
    
    # 기존에 생성된 namespace 에서 중복된 것이 있는지 확인
    print("namespace 목록 : ")
    for ns in namespaces.items:
        if ns.metadata.name == namespace_name:
            print("중복된 namespace 입니다!")
            return "중복된 namespace"

    try:
        # V1 Namespace 객체 생성
        namespace_instance = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace_name))
        
        # Kubernetes API 서버에 namespace 생성 요청
        api_instance = client.CoreV1Api()
        api_instance.create_namespace(body=namespace_instance)
        result = f'{namespace_name} 생성완료'
        return result
    
    # 생성 실패
    except Exception as e:
        return e
        
    
    

if __name__=="__main__":
    result = create_kubernetes_namespace('test1')
    
    print("생성 결과:",result)