import keyring
from datetime import datetime

from services.SRT2 import SRT2
from korail2 import Korail
from SRT.errors import SRTResponseError, SRTLoginError


# 👉 - 최근 로그인한 계정 정보를 가져오는 함수
def get_login(rail_type="SRT"):
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or "",
        "last_login_at": keyring.get_password(rail_type, "last_login_at") or "",
        "last_login_type": keyring.get_password(rail_type, "last_login_type") or "",
    }
    return credentials


def check_login(rail_type="SRT", id="", password=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        temp = SRT2(id, password) if rail_type == "SRT" else Korail(id, password)

        # ℹ️ -  KTX의 경우 로그인 실패시 별도의 예외가 발생하지 않아서 이렇게 처리함
        if rail_type == "KTX":
            if temp.logined:
                keyring.set_password(rail_type, "id", id)
                keyring.set_password(rail_type, "pass", password)
                keyring.set_password(rail_type, "last_login_at", now)
                keyring.set_password(rail_type, "ok", "1")
                return {"status": "success", "msg": "로그인 성공"}
            else:
                return {"status": "fail", "msg": "로그인 실패"}

        keyring.set_password(rail_type, "id", id)
        keyring.set_password(rail_type, "pass", password)
        keyring.set_password(rail_type, "last_login_at", now)
        keyring.set_password(rail_type, "ok", "1")
        return {"status": "success", "msg": "로그인 성공"}

    # ℹ️ - SRT의 경우 로그인 실패시 예외가 발생해서 이렇게 처리함
    except SRTLoginError as err:
        return {"status": "fail", "msg": "로그인 실패"}
    except SRTResponseError as err:
        keyring.delete_password(rail_type, "ok")
        return False


def set_login(rail_type="SRT", id="", password=""):
    try:
        temp = SRT2(id, password) if rail_type == "SRT" else Korail(id, password)
        print(temp)
        print(temp.logined)
        keyring.set_password(rail_type, "id", id)
        keyring.set_password(rail_type, "pass", password)
        keyring.set_password(rail_type, "ok", "1")
        return True
    except SRTResponseError as err:
        keyring.delete_password(rail_type, "ok")
        return False


def login(rail_type="SRT"):
    if (
        keyring.get_password(rail_type, "id") is None
        or keyring.get_password(rail_type, "pass") is None
    ):
        set_login(rail_type)

    user_id = keyring.get_password(rail_type, "id")
    password = keyring.get_password(rail_type, "pass")

    rail = SRT2 if rail_type == "SRT" else Korail
    return rail(user_id, password)
