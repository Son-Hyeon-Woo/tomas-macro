from typing import Awaitable, Callable, List, Optional, Tuple, Union, TypedDict
import keyring


class SetStation(TypedDict):
    id: int
    name: str
    selected: bool


RailType = Union[str, None]
STATIONS = {
    "SRT": [
        "수서",
        "동탄",
        "평택지제",
        "경주",
        "곡성",
        "공주",
        "광주송정",
        "구례구",
        "김천(구미)",
        "나주",
        "남원",
        "대전",
        "동대구",
        "마산",
        "목포",
        "밀양",
        "부산",
        "서대구",
        "순천",
        "여수EXPO",
        "여천",
        "오송",
        "울산(통도사)",
        "익산",
        "전주",
        "정읍",
        "진영",
        "진주",
        "창원",
        "창원중앙",
        "천안아산",
        "포항",
    ],
    "KTX": [
        "서울",
        "용산",
        "영등포",
        "광명",
        "수원",
        "천안아산",
        "오송",
        "대전",
        "서대전",
        "김천구미",
        "동대구",
        "경주",
        "포항",
        "밀양",
        "구포",
        "부산",
        "울산(통도사)",
        "마산",
        "창원중앙",
        "경산",
        "논산",
        "익산",
        "정읍",
        "광주송정",
        "목포",
        "전주",
        "순천",
        "여수EXPO",
        "청량리",
        "강릉",
        "행신",
        "정동진",
    ],
}
DEFAULT_STATIONS = {
    "SRT": ["수서", "대전", "동대구", "부산"],
    "KTX": ["서울", "대전", "동대구", "부산"],
}


def set_station(rail_type: RailType, selected_stations: List[SetStation]) -> bool:
    stations, default_station_key = get_station(rail_type)

    selected_stations = [
        station["name"] for station in selected_stations if station["selected"]
    ]

    if not selected_stations:
        print("선택된 역이 없습니다.")
        return False

    # keyring.set_password(rail_type, "station", ",".join(map(str, selected_stations)))
    keyring.set_password(
        rail_type, "station", (selected_stations := ",".join(selected_stations))
    )
    selected_station_names = ", ".join([selected_stations])
    print(f"선택된 역: {selected_station_names}")

    return True


def get_station(rail_type: RailType) -> Tuple[List[str], List[int]]:
    stations = STATIONS[rail_type]
    station_key = keyring.get_password(rail_type, "station")

    if not station_key:
        return stations, DEFAULT_STATIONS[rail_type]

    valid_keys = [x for x in station_key.split(",")]
    return stations, valid_keys or DEFAULT_STATIONS[rail_type]
