import shutil
import os
import subprocess
import json
import time 

def create_folder(folder_path):                                                       # 사용자 폴더 생성 
    try:
        os.makedirs(folder_path)
        print(f"폴더 생성: {folder_path}")
    except FileExistsError:
        print(f"폴더 이미 존재: {folder_path}")


def copy_folder(source_folder, destination_folder):                                    # templates 복사 
    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"폴더 복사: {destination_folder}")
    except FileNotFoundError:
        print(f"폴더를 찾을 수 없음: {source_folder}")
    except FileExistsError:
        print(f"대상 폴더 이미 존재: {destination_folder}")

def create_and_write_file(file_path, content):                                         # 파일 생성
    with open(file_path, 'w') as file:
        file.write(content)
        print(f"파일 생성 및 문장 추가: {file_path}")


def delete_folder(folder_path):                                                        # 서비스 생성 후 폴더 삭제
    try:
        shutil.rmtree(folder_path)
        print(f"폴더 삭제 완료: {folder_path}")
    except FileNotFoundError:
        print(f"폴더를 찾을 수 없음: {folder_path}")
    except Exception as e:
        print(f"폴더 삭제 중 오류 발생: {e}")


def values(service_name, port, docker_image):                                          # values.yaml 내용

    values = f"ingress:\n  name: \"{service_name}\"\n  namespace: \"{service_name}\"\n\nservice:\n  name: \"{service_name}\"     \n\napp:\n  name: \"{service_name}\"            \n\ncontainer:\n  name: \"{service_name}\"               \n  image: {docker_image}             \n  port: {port}                   \n\nnode:\n  name: \"{service_name}\"         \n  type: t3.medium        \n  dc: 2                  \n  size: 20               \n\nnamespace:\n  name: \"{service_name}\"  \n\ndeployment:\n  name: \"{service_name}\"\n  namespace: \"{service_name}\"\n  rep: 3"
    return values


def chart(service_name, email):                                                         # Chart.yaml 내용

    chart = f"apiVersion: v2\nname: {service_name}\ndescription: {service_name}\n\nkeywords:\n  - rocketdan\n  - rockets\n\nmaintainer:\n  - name: {service_name}\n    email: {email}\nengine: gotpl\n\ntype: application\nversion: 0.1.0"
    return chart


def nodegroup(service_name):                                                            # nodegroup.yaml 내용

    ng = f"apiVersion: eksctl.io/v1alpha5\nkind: ClusterConfig\n\nmetadata:\n  name: eks-rockets\n  region: ap-northeast-2\n\nmanagedNodeGroups:\n  - name: {service_name}\n    labels:\n      nodegroup: {service_name}\n    instanceType: t3.medium\n    desiredCapacity: 1\n    volumesize: 20"
    return ng

def get_nodegroup_status(cluster_name, nodegroup_name):                                         # nodegroup 상태 확인
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
    

def create_eks_nodegroup(path, service_name, cluster):                                            # nodegroup 생성 명령어 실행
    command = f"eksctl create nodegroup --config-file=./{path}/nodegroup.yaml --include={service_name}"
    
    try:
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Nodegroup 생성 명령어 실행 중 오류 발생: {e}")
        delete_eks_nodegroup(service_name, cluster)


def delete_eks_nodegroup(path, service_name, cluster):                                            # nodegroup 생성 명령어 실행
    command = f"eksctl delete nodegroup {service_name} --cluster={cluster}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        create_eks_nodegroup(path, service_name)

    except subprocess.CalledProcessError as e:
        print(f"Nodegroup 삭제 명령어 실행 중 오류 발생: {e}")


def wait_for_nodegroup_deletion(cluster, service_name):                                        # nodegroup 상태 확인 후 있으면 삭제 후 생성, 없으면 생성

    while True:
        status = get_nodegroup_status(cluster, service_name)

        if status == "DELETING":
            print("삭제 중")
            time.sleep(5)

        elif status == "ACTIVE":
            print("삭제 시작")
            delete_eks_nodegroup(cluster, service_name)
            time.sleep(3)
        
        elif status == "CREATING":
            print("생성 오류")
            delete_eks_nodegroup(cluster, service_name)

        elif status == None:
            print("생성 시작")
            time.sleep(60)
            create_eks_nodegroup(service_name, service_name)
            break

        else:
            delete_eks_nodegroup(cluster, service_name)


def delete_namespace(service_name):                                            # nodegroup 생성 명령어 실행
    command = f"kubectl delete namespace {service_name} --force --grace-period=0"
    
    try:
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Nodegroup 생성 명령어 실행 중 오류 발생: {e}")


def create_service(service_name, image, port, email):

    target_folder = service_name
    create_folder(target_folder)

    source_folder = "templates"
    destination_folder = os.path.join(target_folder, "./templates")
    copy_folder(source_folder, destination_folder)
    values_yaml = os.path.join(target_folder, "values.yaml")
    chart_yaml = os.path.join(target_folder, "Chart.yaml")
    nodegroup_yaml = os.path.join(target_folder, "nodegroup.yaml")

    values_content = values(service_name, port, image)
    chart_content = chart(service_name, email)
    nodegroup_content = nodegroup(service_name)
    create_and_write_file(values_yaml, values_content)
    create_and_write_file(chart_yaml, chart_content)
    create_and_write_file(nodegroup_yaml, nodegroup_content)


def helm_delete(service_name):
    command = f"helm uninstall {service_name}"
    try:
        delete_namespace(service_name)
        subprocess.run(command, shell=True, check=True)
        helm_start(service_name)

    except subprocess.CalledProcessError as e:
        print(f"helm 삭제 중 오류 발생: {e}")
        delete_folder(service_name)


def helm_start(service_name):                                          # helm repo가 잘 생성되면 폴더 삭제 
    command = f"helm install {service_name} {service_name}/"
    try:
        subprocess.run(command, shell=True, check=True)
        delete_folder(service_name)

    except subprocess.CalledProcessError as e:
        print(f"helm 실행 중 오류 발생: {e}")
        helm_delete(service_name)    


def get_load_balancer_dns(service_name):                               # 생성한 Load Balancer DNS 주소 가져오기 
    try:
        # AWS CLI를 사용하여 ELB 정보 조회
        command = f"aws elbv2 describe-load-balancers --names {service_name}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        # JSON 형식으로 반환된 결과 파싱
        response_json = json.loads(result.stdout)
        load_balancer_dns = response_json['LoadBalancers'][0]['DNSName']

        return load_balancer_dns
    
    except subprocess.CalledProcessError as e:
        print(f"에러: {e}")
        return None
    


if __name__ == "__main__":

    service_name = "trytest13"
    image = "pengbai/docker-supermario"
    port = 8080
    email = "aaa@aaa.aaa"
    cluster = "eks-rockets"
    delete_folder(service_name)
    create_service(service_name, image, port, email)
    create_eks_nodegroup(service_name, service_name, cluster)
    helm_start(service_name)
    time.sleep(10)                                   # 바로 LB 못 불러와서 잠시 후 불러오기 위해서
    print(get_load_balancer_dns(service_name))
