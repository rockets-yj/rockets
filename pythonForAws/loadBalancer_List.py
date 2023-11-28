import boto3

session = boto3.Session (
    
    aws_access_key_id = '',
    aws_secret_access_key= '',
    region_name= ''
)


def get_classic_lb_info(aws_region='us-west-2'):
    # Boto3 ELB 클라이언트 생성
    elb_client = boto3.client('elbv2', region_name=aws_region)

    try:
        # Classic Load Balancer에 대한 정보 가져오기
        response = elb_client.describe_load_balancers()

        # 가져온 정보를 이용하여 필요한 데이터 출력
        classic_load_balancers = response['LoadBalancers']
        print("Classic Load Balancer")
        print(classic_load_balancers)
        for classic_lb in classic_load_balancers:
            print(f"- Load Balancer Name: {classic_lb['LoadBalancerName']}")
            print(f"  - DNS Name: {classic_lb['DNSName']}")
            print(f"  - Load Balancer ARN: {classic_lb['LoadBalancerArn']}")
            print("\n")
        
        
        # Classic Load Balancer의 인스턴스 목록 가져오기
        # instances = classic_lb.get('Instances', [])
        # if instances:
        #     print("Instances:")
        #     for instance in instances:
        #         print(f"- Instance ID: {instance['InstanceId']}")
        # else:
        #     print("No instances associated with this Classic Load Balancer.")
            
        print("\n")
    except Exception as e:
        print(f"Error: {e}")


def get_elb_load_balancers(aws_region='us-west-2'):
    # Boto3 ELB 클라이언트 생성
    elb_client = boto3.client('elbv2', region_name=aws_region)

    try:
        # ELB 로드 밸런서 목록 가져오기
        response = elb_client.describe_load_balancers()
        
        # 가져온 정보를 이용하여 필요한 데이터 출력
        load_balancers = response['LoadBalancers']
        print("Elastic Load Balancers:")
        for lb in load_balancers:
            print(f"- Load Balancer Name: {lb['LoadBalancerName']}")
            print(f"  - DNS Name: {lb['DNSName']}")
            print(f"  - Load Balancer ARN: {lb['LoadBalancerArn']}")
            print(lb)
            print("\n")
    except Exception as e:
        print(f"Error: {e}")

def get_alb_load_balancers(aws_region='us-west-2'):
    # Boto3 ALB 클라이언트 생성
    alb_client = boto3.client('elbv2', region_name=aws_region)

    try:
        # ALB 로드 밸런서 목록 가져오기
        response = alb_client.describe_load_balancers()
        
        # 가져온 정보를 이용하여 필요한 데이터 출력
        load_balancers = response['LoadBalancers']
        print("Application Load Balancers:")
        for lb in load_balancers:
            print(f"- Load Balancer Name: {lb['LoadBalancerName']}")
            print(f"  - DNS Name: {lb['DNSName']}")
            print(f"  - Load Balancer ARN: {lb['LoadBalancerArn']}")
            print(lb)
            print("\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # AWS 리전 설정
    region = "ap-northeast-2"

    # ELB 로드 밸런서 목록 가져오기
    get_elb_load_balancers(region)

    # ALB 로드 밸런서 목록 가져오기
    get_alb_load_balancers(region)
    
    # CLB 로드 밸런서 목록 가져오기
    get_classic_lb_info(region)
