import inquirer  # ℹ️ - cmd에서 대화식으로 질문을 던지고 답변을 받는 라이블러리
import keyring


from services.SRT2 import SRT2
from korail2 import Korail
from SRT.errors import SRTResponseError


def get_login(rail_type="SRT"):
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or "",
        "last_login_at": keyring.get_password(rail_type, "last_login_at") or "",
    }
    return credentials


def set_login(rail_type="SRT", id="", password=""):
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or "",
    }

    try:
        temp = SRT2(id, password) if rail_type == "SRT" else Korail(id, password)
        print(temp)

        keyring.set_password(rail_type, "id", id)
        keyring.set_password(rail_type, "pass", password)
        keyring.set_password(rail_type, "ok", "1")
        return True
    except SRTResponseError as err:
        print(err)
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
