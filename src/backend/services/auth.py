import inquirer  # ℹ️ - cmd에서 대화식으로 질문을 던지고 답변을 받는 라이블러리
import keyring


from services.SRT2 import SRT2
from korail2 import Korail
from SRT.errors import SRTResponseError


def get_login(rail_type="SRT"):
    print(rail_type)
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or "",
        "last_login_at": keyring.get_password(rail_type, "last_login_at") or "",
    }

    return credentials


def set_login(rail_type="SRT"):
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or "",
    }

    login_info = inquirer.prompt(
        [
            inquirer.Text(
                "id",
                message=f"{rail_type} 계정 아이디 (멤버십 번호, 이메일, 전화번호)",
                default=credentials["id"],
            ),
            inquirer.Password(
                "pass",
                message=f"{rail_type} 계정 패스워드",
                default=credentials["pass"],
            ),
        ]
    )
    if not login_info:
        return False

    try:
        (
            SRT2(login_info["id"], login_info["pass"])
            if rail_type == "SRT"
            else Korail(login_info["id"], login_info["pass"])
        )

        keyring.set_password(rail_type, "id", login_info["id"])
        keyring.set_password(rail_type, "pass", login_info["pass"])
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
