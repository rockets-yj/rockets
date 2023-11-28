import docker


def deleteDockerImage(image_name,image_tag):
    try:
        # Docker 클라이언트 생성
        client = docker.from_env()
        
        # 이미지 삭제
        client.images.remove(image_name+":"+image_tag)
        print(f'Docker 이미지 {image_name} : {image_tag} 삭제 완료')
    except Exception as e:
        print(f"이미지 삭제 중 에러 : {e}")
        
if __name__ == '__main__':
    deleteDockerImage('testdocker','latest')
    pass