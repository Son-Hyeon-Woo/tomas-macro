import eel
import os
from dotenv import load_dotenv
from services.auth import get_login, set_login, check_login
from services.station import get_station, set_station
from services.reserve import get_default_reservation, search_train
import time
import threading

# Eel 초기화 및 웹 파일 디렉토리 설정
# Svelte 빌드 파일은 'web' 디렉토리에 있다고 가정
# eel.init("web")

# .env 파일 로드
load_dotenv()

# 👉 - 이전 로그인 정보 가져오는 함수
eel.expose(get_login)
eel.expose(set_login)
eel.expose(check_login)
eel.expose(get_station)
eel.expose(set_station)
eel.expose(get_default_reservation)
eel.expose(search_train)


# Python에서 JavaScript로 호출할 함수
@eel.expose
def say_hello_from_python(name):
    return f"Hello {name} from Python!"


# JavaScript에서 호출될 Python 함수
@eel.expose
def get_system_info():
    return {"os": os.name, "platform": os.sys.platform, "cwdss": os.getcwd()}


# 👉 - for 비동기 처리
def do_test():
    print(dir(eel))
    cnt = 0
    while cnt < 5:
        time.sleep(1)
        cnt += 1
        print("test", cnt)
        eel.update_status(cnt)()


@eel.expose
def start_reservation():
    for i in range(5):
        status = {
            "current_step": i,
            "message": f"예약 진행 중... 단계 {i+1}/5",
            "is_completed": False,
        }
        # JavaScript 함수 호출 시 콜백으로 처리
        eel.update_status(status, _callback=lambda: None)
        eel.sleep(1)  # time.sleep 대신 eel.sleep 사용

    final_status = {"current_step": 5, "message": "예약 완료!", "is_completed": True}
    eel.update_status(final_status, _callback=lambda: None)


@eel.expose
def handle_request():
    threading.Thread(target=do_test).start()


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
            # start 전에 JavaScript가 초기화될 시간을 주기 위해 잠시 대기
            # eel.start("index.html", block=False)
            time.sleep(2)  # JavaScript가 로드되고 함수가 expose될 시간을 줌

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
