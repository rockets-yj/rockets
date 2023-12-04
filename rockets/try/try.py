import shutil
import os
import subprocess

def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"폴더 생성: {folder_path}")
    except FileExistsError:
        print(f"폴더 이미 존재: {folder_path}")

def copy_folder(source_folder, destination_folder):
    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"폴더 복사: {destination_folder}")
    except FileNotFoundError:
        print(f"폴더를 찾을 수 없음: {source_folder}")
    except FileExistsError:
        print(f"대상 폴더 이미 존재: {destination_folder}")

def values(service_name, port, docker_image):

    values = f"ingress:\n  name: {service_name}\n  namespace: {service_name}\n\nservice:\n  name: {service_name}     \n\napp:\n  name: {service_name}            \n\ncontainer:\n  name: {service_name}               \n  image: {docker_image}             \n  port: {port}                   \n\nnode:\n  name: {service_name}         \n  type: t3.medium        \n  dc: 2                  \n  size: 20               \n\nnamespace:\n  name: {service_name}  \n  namespace: {service_name}\n  rep: 3"
    return values

def chart(service_name, email):

    chart = f"apiVersion: v2\nname: {service_name}\ndescription: {service_name}\n\nkeywords:\n  - rocketdan\n  - rockets\n\nmaintainer:\n  - name: {service_name}\n    email: {email}\nengine: gotpl\n\ntype: application\nversion: 0.1.0"
    return chart

def nodegroup(service_name):

    ng = f"apiVersion: eksctl.io/v1alpha5\nkind: ClusterConfig\n\nmetadata:\n  name: rockets-eks\n  region: ap-northeast-2\n\nmanagedNodeGroups:\n  - name: {service_name}\n    labels:\n      nodegroup: {service_name}\n    instanceType: t3.medium\n    desiredCapacity: 1\n    volumesize: 20"
    return ng

def create_and_write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        print(f"파일 생성 및 문장 추가: {file_path}")

def create_eks_nodegroup(path, service_name):
    command = f"eksctl create nodegroup --config-file=./{path}/nodegroup.yaml --include={service_name}"
    
    try:
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Nodegroup 생성 명령어 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    # 폴더 생성
    target_folder = "test2"
    create_folder(target_folder)

    source_folder = "templates"
    destination_folder = os.path.join(target_folder, "./templates")
    copy_folder(source_folder, destination_folder)

    values_yaml = os.path.join(target_folder, "values.yaml")
    chart_yaml = os.path.join(target_folder, "Chart.yaml")
    nodegroup_yaml = os.path.join(target_folder, "nodegroup.yaml")
    service_name = "trytest0901"
    image = "image"
    port = 80
    email = "aaa@aaa.aaa"
    values_content = values(service_name, port, image)
    chart_content = chart(service_name, email)
    nodegroup_content = nodegroup(service_name)
    create_and_write_file(values_yaml, values_content)
    create_and_write_file(chart_yaml, chart_content)
    create_and_write_file(nodegroup_yaml, nodegroup_content)
    create_eks_nodegroup(target_folder, service_name)