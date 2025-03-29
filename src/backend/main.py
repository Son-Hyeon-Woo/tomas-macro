import eel
import os
from bottle import Bottle, static_file
from dotenv import load_dotenv
from module.srtgo import get_login, set_login, check_login
from module.srtgo import get_station, set_station

from module.srtgo import get_train_list, reserve
import time
import threading

app = Bottle()


static_dir = os.path.join(os.getcwd(), "dist")


# .env 파일 로드
load_dotenv()

# # 👉 - 이전 로그인 정보 가져오는 함수
eel.expose(get_login)
eel.expose(set_login)
eel.expose(check_login)
eel.expose(get_station)
eel.expose(set_station)
eel.expose(get_train_list)
eel.expose(reserve)


@eel.expose
def spawnTest():

    print(eel)

    print("====================")

    print(eel._exposed_functions)
    print(eel._js_functions)

    print("====================")

    def do_loop():
        count = 0
        while True:
            print(count, "회차: spawnTest")
            # eel.sleep(1)
            eel.updateStatus(count + "회차: spawnTest")
            count += 1
            eel.sleep(1)

    eel.spawn(do_loop)


# 앱 시작
def start_app():

    try:
        # 환경변수 가져오기

        # 프로덕션 모드
        eel.init("dist")

        # 정적 파일 제공 라우트
        @app.route("/assets/<filepath:path>")
        def serve_static(filepath):
            return static_file(filepath, root="dist/assets")

        # 모든 경로를 index.html로 리다이렉트하여 SPA 지원
        @app.route("/<:re:.*>")
        def catch_all():
            return static_file("index.html", root="dist")

        # Eel의 기본 라우트를 사용자 정의 Bottle 인스턴스에 등록
        eel.register_eel_routes(app)

        time.sleep(2)
        eel.start(
            "",
            app=app,
            size=(1000, 800),
            mode="default",
        )

    except EnvironmentError:
        print("Chrome browser not found. Starting in default browser mode.")
        # 크롬을 찾을 수 없는 경우 기본 브라우저로 실행
        eel.start("index.html", mode="default")


if __name__ == "__main__":
    start_app()
