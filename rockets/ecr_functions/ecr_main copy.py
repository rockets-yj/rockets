from . import *


if __name__ == '__main__':
    service_name = 'mario' # 나중에 DB에서 가져올것
    ecr_create_test(service_name) # 여기서 db에다가 ecr_uri 를 바로 넣음 -차후 목표 DB에서 해당 서비스 이름으로 검색을 해서 그 서비스 테이블에 ecr_uri 주소 넣기
    dockerBuild(service_name) # 여기서 태그 넣는것도 해도 됨, 따로 태그를 넣는 파이썬 파일을 만들어도 됨
    # dockerpush(service_name) # db 검색을 해서, 해당 service_name 의 uri 주소를 가져옴 - ecr_uri/servie_name:latest
    # 목록을 조회한다.
    # ecr_delete_test(service_name) # 해당 ecr 이 삭제됨
    # 삭제되었는지 한번 더 조회

