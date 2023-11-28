import boto3

def get_eks_node_groups(eks_cluster_name, aws_region='ap-northeast-2'):
    # Boto3 EKS 클라이언트 생성
    eks_client = boto3.client('eks', region_name=aws_region)

    try:
        # EKS 클러스터에 대한 노드 그룹 목록 가져오기
        response = eks_client.list_nodegroups(clusterName=eks_cluster_name)
        
        
        
        
        # 노드 그룹 목록 출력
        node_groups = response['nodegroups']
        print(f"EKS Cluster: {eks_cluster_name}")
        print("Node Groups:")
        for node_group in node_groups:
            print(f"- {node_group}")
            node_group_info = eks_client.describe_nodegroup(clusterName=eks_cluster_name, nodegroupName=node_group)
            print(node_group_info)
            
            # 필요한 정보 출력 (원하는 정보에 따라 조정 가능)
            print(f"  - Status: {node_group_info['nodegroup']['status']}")
            print(f"  - Scaling Config: {node_group_info['nodegroup']['scalingConfig']}")
            print(f"  - Disk Size: {node_group_info['nodegroup']['diskSize']}")
            # 더 많은 정보를 가져오고 싶다면 node_group_info를 확인하여 필요한 정보를 추가하세요.
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # EKS 클러스터 이름 및 AWS 리전 설정
    cluster_name = "eks-demo"
    
    # EKS 노드 그룹 목록 가져오기
    get_eks_node_groups(cluster_name)