import os
from django.conf import settings

def delete_local_media_file(file_path):
    # 로컬 media 경로 설정
    media_root = settings.MEDIA_ROOT

    # 파일의 절대 경로 생성
    absolute_file_path = os.path.join(media_root, file_path)

    try:
        # 파일 삭제
        os.remove(absolute_file_path)
        print(f'파일이 삭제되었습니다: {absolute_file_path}')
        return True
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {absolute_file_path}')
        return False
    except Exception as e:
        print(f'파일 삭제 중 오류 발생: {e}')
        return False


# 삭제할 파일의 상대 경로 (예: 'uploads/example.txt')
file_to_delete = 'test231204.zip'

# 로컬 media 폴더에서 파일 삭제
delete_local_media_file(file_to_delete)
