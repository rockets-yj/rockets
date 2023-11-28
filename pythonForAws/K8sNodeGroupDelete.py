import boto3

def delete_node_group(cluster_name, nodegroup_name):
    eks_client = boto3.client('eks')

    # 노드 그룹 삭제 요청
    response = eks_client.delete_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)

    # 삭제 결과 확인
    print(response)

if __name__ == '__main__':
    cluster_name = 'eks-demo'
    nodegroup_name = 'hwang3'

    # 노드 그룹 삭제
    delete_node_group(cluster_name, nodegroup_name)