import shutil
import os

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

def create_and_write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        print(f"파일 생성 및 문장 추가: {file_path}")

if __name__ == "__main__":
    # 폴더 생성
    target_folder = "test2"
    create_folder(target_folder)

    source_folder = "templates"
    destination_folder = os.path.join(target_folder, "./templates")
    copy_folder(source_folder, destination_folder)

    values_yaml = os.path.join(target_folder, "values.yaml")
    chart_yaml = os.path.join(target_folder, "Chart.yaml")
    service_name = "test"
    image = "image"
    port = 80
    email = "aaa@aaa.aaa"
    values_content = values(service_name, port, image)
    chart_content = chart(service_name, email)
    create_and_write_file(values_yaml, values_content)
    create_and_write_file(chart_yaml, chart_content)