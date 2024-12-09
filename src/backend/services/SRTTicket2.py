from SRT.reservation import SRTTicket


class SRTTicket2(SRTTicket):
    DISCOUNT_TYPE = {
        "000": "어른/청소년",
        "101": "탄력운임기준할인",
        "105": "자유석 할인",
        "106": "입석 할인",
        "107": "역방향석 할인",
        "108": "출입구석 할인",
        "109": "가족석 일반전환 할인",
        "111": "구간별 특정운임",
        "112": "열차별 특정운임",
        "113": "구간별 비율할인(기준)",
        "114": "열차별 비율할인(기준)",
        "121": "공항직결 수색연결운임",
        "131": "구간별 특별할인(기준)",
        "132": "열차별 특별할인(기준)",
        "133": "기본 특별할인(기준)",
        "191": "정차역 할인",
        "192": "매체 할인",
        "201": "어린이",
        "202": "동반유아 할인",
        "204": "경로",
        "205": "1~3급 장애인",
        "206": "4~6급 장애인",
    }

    def __init__(self, data):
        self.car = data["scarNo"]
        self.seat = data["seatNo"]
        self.seat_type_code = data["psrmClCd"]
        self.seat_type = self.SEAT_TYPE[self.seat_type_code]
        self.passenger_type_code = data["dcntKndCd"]
        if self.passenger_type_code in self.DISCOUNT_TYPE:
            self.passenger_type = self.DISCOUNT_TYPE[self.passenger_type_code]
        else:
            self.passenger_type = "기타 할인"

        self.price = int(data["rcvdAmt"])
        self.original_price = int(data["stdrPrc"])
        self.discount = int(data["dcntPrc"])
