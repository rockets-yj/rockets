import boto3

session = boto3.Session (
    
    aws_access_key_id = '',
    aws_secret_access_key= '',
    region_name= ''
)



def create_node_group(cluster_name, nodegroup_name, **kwargs):
    eks_client = boto3.client('eks')
    
    # 노드 그룹 생성에 필요한 파라미터 설정 * 이 달린 부분은 필수 설정
    managed_nodegroup_params = {
        'clusterName': cluster_name,        # 노드를 생성할 클러스터 이름 *
        'nodegroupName': nodegroup_name,    # 생성할 노드그룹의 이름 *
        'scalingConfig': {  # 노드 그룹의 크기 지정
            'minSize': 1,   # 최소 크기
            'maxSize': 2,   # 최대 크기
            'desiredSize':1 # 기본적으로 유지되는 크기
        },
        # 서브넷 주소 *
        'subnets': ['subnet-0e35331677c1b6bc8','subnet-03aacf0d6aa4005b8', 'subnet-02fd06bddaf5864eb' ],
        # 노드 규칙 *
        'nodeRole': 'arn:aws:iam::610264642862:role/eksctl-eks-demo-nodegroup-hwangloc-NodeInstanceRole-INTdUnPWLZny',
        'instanceTypes': ['t2.micro'], # 사용할 인스턴스 타입 유형
        'diskSize':20, # 각 노드의 EBS 볼륨 크기
        'remoteAccess':{
            'ec2SshKey': 'rocket'
        }
        
    }
    
    response = eks_client.create_nodegroup(**managed_nodegroup_params)
    
    print(response)
    

if __name__ == '__main__':
    create_node_group('eks-demo','hwang3')