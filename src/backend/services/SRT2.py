from SRT import SRT
from SRT.passenger import (
    Passenger,
    Adult,
    Child,
    Senior,
    Disability1To3,
    Disability4To6,
)
from SRT.train import SRTTrain
from SRT import constants

from datetime import datetime
from SRT.response_data import SRTResponseData
from SRT.errors import SRTResponseError, SRTNotLoggedInError
from SRT.reservation import SRTReservation
from services.SRTTicket2 import SRTTicket2


class SRT2(SRT):
    def search_train(
        self,
        dep: str,
        arr: str,
        date: str | None = None,
        time: str | None = None,
        time_limit: str | None = None,
        passengers: list[Passenger] | None = None,
        available_only: bool = True,
    ) -> list[SRTTrain]:
        """주어진 출발지에서 도착지로 향하는 SRT 열차를 검색합니다.

        Args:
            dep (str): 출발역
            arr (str): 도착역
            date (str, optional): 출발 날짜 (yyyyMMdd) (default: 당일)
            time (str, optional): 출발 시각 (hhmmss) (default: 0시 0분 0초)
            time_limit (str, optional): 출발 시각 조회 한도 (hhmmss)
            passengers (list[:class:`Passenger`], optional): 예약 인원 (default: 어른 1명)
            available_only (bool, optional): 매진되지 않은 열차만 검색합니다 (default: True)

        Returns:
            list[:class:`SRTTrain`]: 열차 리스트
        """

        if dep not in constants.STATION_CODE or arr not in constants.STATION_CODE:
            raise ValueError(f'Invalid station: "{dep}" or "{arr}"')

        dep_code, arr_code = constants.STATION_CODE[dep], constants.STATION_CODE[arr]
        date = date or datetime.now().strftime("%Y%m%d")
        time = time or "000000"

        passengers = passengers or [Adult()]
        passengers = Passenger.combine(passengers)
        passengers_count = str(Passenger.total_count(passengers))

        data = {
            "chtnDvCd": "1",
            "arriveTime": "N",
            "seatAttCd": "015",
            "psgNum": passengers_count,
            "trnGpCd": 109,
            "stlbTrnClsfCd": "05",
            "dptDt": date,
            "dptTm": time,
            "arvRsStnCd": arr_code,
            "dptRsStnCd": dep_code,
        }

        r = self._session.post(
            url=constants.API_ENDPOINTS["search_schedule"], data=data
        )
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())
        all_trains = parser.get_all()["outDataSets"]["dsOutput1"]
        trains = [SRTTrain(train) for train in all_trains]
        trains = [train for train in trains if train.train_name == "SRT"]

        if available_only:
            trains = [t for t in trains if t.seat_available()]

        if time_limit:
            trains = [t for t in trains if t.dep_time <= time_limit]

        return trains

    def ticket_info(self, reservation: SRTReservation | int) -> list[SRTTicket2]:
        if not self.is_login:
            raise SRTNotLoggedInError()

        if isinstance(reservation, SRTReservation):
            reservation = reservation.reservation_number

        url = constants.API_ENDPOINTS["ticket_info"]
        data = {"pnrNo": reservation, "jrnySqno": "1"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        tickets = [SRTTicket2(ticket) for ticket in parser.get_all()["trainListMap"]]

        return tickets
