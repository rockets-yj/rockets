import subprocess
import json
import time

def get_nodegroup_status(cluster_name, nodegroup_name):
    try:
        # AWS CLI를 사용하여 노드 그룹 정보 조회
        command = f"aws eks describe-nodegroup --cluster-name {cluster_name} --nodegroup-name {nodegroup_name}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        # JSON 형식으로 반환된 결과 파싱
        response_json = json.loads(result.stdout)
        status = response_json['nodegroup']['status']
        return status
    except subprocess.CalledProcessError as e:
        print(f"에러: {e}")
        return None
    
def create_eks_nodegroup(nodegroup_name):                                            # nodegroup 생성 명령어 실행
    command = f"eksctl create nodegroup --config-file=./{nodegroup_name}/nodegroup.yaml --include={nodegroup_name}"
    
    try:
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Nodegroup 생성 명령어 실행 중 오류 발생: {e}")
        #delete_nodegroup(service_name, cluster)

def delete_nodegroup(cluster_name, nodegroup_name):
    try:
        # AWS CLI를 사용하여 노드 그룹 삭제
        command = f"eksctl delete nodegroup {nodegroup_name} --cluster={cluster_name}"
        subprocess.run(command, shell=True, check=True)
        print(f"노드 그룹 삭제 완료: {nodegroup_name}")
    except subprocess.CalledProcessError as e:
        print(f"에러: {e}")

def wait_for_nodegroup_deletion(cluster_name, nodegroup_name, timeout_seconds=10):

    while True:
        status = get_nodegroup_status(cluster_name, nodegroup_name)

        if status == "DELETING":
            time.sleep(5)
        
        elif status == None:
            create_eks_nodegroup(nodegroup_name)
            break

        else:
            break

if __name__ == "__main__":
    eks_cluster_name = 'rockets-eks'
    nodegroup_name = 'trytest11'

    # 노드 그룹 상태 확인
    nodegroup_status = get_nodegroup_status(eks_cluster_name, nodegroup_name)

    if nodegroup_status == "ACTIVE":
        print("노드 그룹이 활성화되어 있습니다. 노드 그룹을 삭제합니다.")
        delete_nodegroup(eks_cluster_name, nodegroup_name)
        create_eks_nodegroup()
    elif nodegroup_status == "DELETING":
        print("노드 그룹이 이미 삭제 중입니다. 대기합니다.")
        wait_for_nodegroup_deletion(eks_cluster_name, nodegroup_name)

    elif nodegroup_status == None:
        create_eks_nodegroup(nodegroup_name)
    else:
        print(f"노드 그룹 상태: {nodegroup_status}")