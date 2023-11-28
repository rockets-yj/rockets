import subprocess
import json


# 각각의 결과를 json 형식으로 가져옴

# helm repo list
def get_helm_chart_list():
    try:
        # Helmo repo 목록을 json 형식으로 가져온다.
        result = subprocess.run(['helm','repo','list','--output','json'], capture_output=True, text=True)
        
        
        # Json 문자열을 파이썬 객체로 변환
        repo_list = json.loads(result.stdout)
        
        for repo in repo_list:
            print(f"Name : {repo['name']} , URL : {repo['url']}")
        
    except Exception as e :
        print(f'실패 : {e}')
    

# helm search repo
def get_helm_repo_list():
    try:
        # Helmo repo 목록을 json 형식으로 가져온다.
        result = subprocess.run(['helm','search','repo','--output','json'], capture_output=True, text=True)
        
        
        # Json 문자열을 파이썬 객체로 변환
        repo_list = json.loads(result.stdout)
        
        for repo in repo_list:
            print(f"Name : {repo['name']} , Chart Version: {repo['version']}, Description: {repo['description']}")
        
    except Exception as e :
        print(f'실패 : {e}')



if __name__ == '__main__':
    get_helm_chart_list()
    get_helm_repo_list()