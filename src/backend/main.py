# main.py
import eel
import os

# Eel 초기화 및 웹 파일 디렉토리 설정
# Svelte 빌드 파일은 'web' 디렉토리에 있다고 가정


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
    try:
        # 개발 모드에서는 chrome-app 모드로 실행
        # eel.start("index.html", mode="chrome-app", size=(800, 600))
        # 개발 모드: Svelte 개발 서버 사용 (기본 포트 5173)
        eel.init("src/frontend")
        eel.start(
            {"port": 5173},
            host="localhost",
            mode="chrome-app",
            size=(800, 600),
        )
        # eel.start("http://localhost:5173", mode="chrome", block=True)
    except EnvironmentError:
        # 크롬을 찾을 수 없는 경우 기본 브라우저로 실행
        eel.init("dist")
        eel.start("index.html", mode="default", size=(800, 600))


if __name__ == "__main__":
    start_app()
