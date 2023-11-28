import docker

def build_docker_image(image_name, dockerfile_path="."):
    client  = docker.from_env()
    
    # docker 이미지 무조건 영어 소문자
    try:
        # Docker 이미지 빌드
        image, build_logs = client.images.build(
            path=dockerfile_path,
            tag=image_name,
            rm=True # 중간 이미지 삭제
        )
        print(f"Docker 이미지 {image_name}이(가) 성공적으로 빌드되었습니다.")
        
    except Exception as e:
        print(f"Docker 이미지 빌드 중 오류가 발생: {e}")

if __name__ == '__main__':
    build_docker_image('testdocker','/home/rocket/hwangdemo/hello-helm')