import boto3

def get_instance_info(instance_id, aws_region='ap-northeast-2'):
    # Boto3 EC2 클라이언트 생성
    ec2_client = boto3.client('ec2', region_name=aws_region)

    try:
        # EC2 인스턴스에 대한 정보 가져오기
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        
        # 가져온 정보를 이용하여 필요한 데이터 출력
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance Name: {get_instance_name(instance)}")
                print(f"Instance State: {instance['State']['Name']}")
                print("\n")
    except Exception as e:
        print(f"Error: {e}")

def get_instance_name(instance):
    # EC2 인스턴스의 태그에서 'Name' 태그 값을 찾아 반환
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return ""


def get_all_instances_info(aws_region='ap-northeast-2'):
    # Boto3 EC2 클라이언트 생성
    ec2_client = boto3.client('ec2', region_name=aws_region)

    try:
        # 모든 EC2 인스턴스에 대한 정보 가져오기
        response = ec2_client.describe_instances()
        print('in all try')
        
        
        # 가져온 정보를 이용하여 필요한 데이터 출력
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(f"Instance ID: {instance['InstanceId']}")
                print(f"Instance Name: {get_instance_name(instance)}")
                print(f"Instance State: {instance['State']['Name']}")
                print(instance)
                
                print("\n")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # EC2 인스턴스 ID 설정
    instance_id = "your-instance-id"
    
    # EC2 인스턴스 정보 가져오기
    #get_instance_info(instance_id)
    get_all_instances_info()
    
