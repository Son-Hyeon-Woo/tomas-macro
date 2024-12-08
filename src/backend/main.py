# main.py
import eel
import os
from dotenv import load_dotenv

# Eel 초기화 및 웹 파일 디렉토리 설정
# Svelte 빌드 파일은 'web' 디렉토리에 있다고 가정
# eel.init("web")

# .env 파일 로드
load_dotenv()


# Python에서 JavaScript로 호출할 함수
@eel.expose
def say_hello_from_python(name):
    return f"Hello {name} from Python!"


# JavaScript에서 호출될 Python 함수
@eel.expose
def get_system_info():
    return {"os": os.name, "platform": os.sys.platform, "cwdss": os.getcwd()}


# 앱 시작
def start_app():
    # .env 파일 로드
    dev_mode = os.getenv("DEV_MODE", "False").lower() == "true"

    try:
        # 환경변수 가져오기
        dev_mode = os.getenv("DEV_MODE", "False").lower() == "true"
        port = int(os.getenv("PORT", 8000))

        if dev_mode:
            print("Development mode")
            # 개발 모드
            eel.init("dist")
            eel.start("index.html", mode="default")

        else:
            print("Production mode")
            # 프로덕션 모드
            eel.init("dist")
            eel.start("index.html")

    except EnvironmentError:
        print("Chrome browser not found. Starting in default browser mode.")
        # 크롬을 찾을 수 없는 경우 기본 브라우저로 실행
        eel.start("index.html", mode="default")


if __name__ == "__main__":
    start_app()
