class SeatStore:
    """좌석 예약 상태를 인메모리로 관리하는 저장소입니다.

    각 좌석은 `seat_id`를 key로 가지고, 예약자 이름 또는 None을 value로 가집니다.
    value가 None이면 예약 가능한 좌석이고, 문자열이면 해당 이름으로 예약된 좌석입니다.
    """

    def __init__(self, seat_ids):
        """좌석 ID 목록을 받아 초기 좌석 상태를 생성합니다.

        Args:
            seat_ids: 예약 시스템에서 사용할 좌석 ID 목록입니다.
        """
        # 모든 좌석은 처음에 예약되지 않은 상태(None)로 초기화합니다.
        self._seats = {seat_id: None for seat_id in seat_ids}

    def list_seats(self):
        """전체 좌석의 예약 상태를 반환합니다.

        Returns:
            좌석 ID와 예약자 이름의 쌍을 담은 dict_items 객체입니다.
            예약되지 않은 좌석은 예약자 이름이 None입니다.
        """
        return self._seats.items()

    def reserve(self, seat_id, name):
        """특정 좌석을 사용자 이름으로 예약합니다.

        Args:
            seat_id: 예약할 좌석 ID입니다.
            name: 좌석을 예약할 사용자 이름입니다.

        Returns:
            예약된 좌석 ID와 예약자 이름을 tuple로 반환합니다.

        Raises:
            ValueError: 이미 예약된 좌석인 경우 발생합니다.
            ValueError: 존재하지 않는 좌석 ID인 경우 발생합니다.
        """
        current = self._get(seat_id)

        # 이미 예약자가 있으면 같은 좌석을 다시 예약할 수 없습니다.
        if current is not None:
            raise ValueError("Seat is already reserved.")

        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        """특정 좌석의 예약을 취소합니다.

        Args:
            seat_id: 예약을 취소할 좌석 ID입니다.
            name: 예약자 이름입니다. 지정된 경우 기존 예약자 이름과 일치해야 합니다.

        Returns:
            예약 취소된 좌석 ID와 None을 tuple로 반환합니다.

        Raises:
            ValueError: 예약되지 않은 좌석인 경우 발생합니다.
            ValueError: 예약자 이름이 일치하지 않는 경우 발생합니다.
            ValueError: 존재하지 않는 좌석 ID인 경우 발생합니다.
        """
        current = self._get(seat_id)

        # 예약되지 않은 좌석은 취소할 수 없습니다.
        if current is None:
            raise ValueError("Seat is not reserved.")

        # 이름이 주어진 경우, 실제 예약자와 일치할 때만 취소를 허용합니다.
        if name and current != name:
            raise ValueError("Name does not match the reservation.")

        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        """특정 좌석의 현재 예약 상태를 반환합니다.

        Args:
            seat_id: 상태를 확인할 좌석 ID입니다.

        Returns:
            좌석 ID와 현재 예약자 이름을 tuple로 반환합니다.
            예약되지 않은 좌석이면 예약자 이름은 None입니다.

        Raises:
            ValueError: 존재하지 않는 좌석 ID인 경우 발생합니다.
        """
        return seat_id, self._get(seat_id)

    def stats(self):
        """전체 좌석 수, 예약된 좌석 수, 예약 가능한 좌석 수를 계산합니다.

        Returns:
            total, reserved, available 값을 담은 dictionary입니다.
        """
        # 예약자 이름이 있는 좌석만 예약된 좌석으로 계산합니다.
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)

        return {"total": total, "reserved": reserved, "available": total - reserved}

    def _get(self, seat_id):
        """좌석 ID에 해당하는 현재 예약자 이름을 반환합니다.

        Args:
            seat_id: 조회할 좌석 ID입니다.

        Returns:
            예약자 이름을 반환합니다.
            예약되지 않은 좌석이면 None을 반환합니다.

        Raises:
            ValueError: 존재하지 않는 좌석 ID인 경우 발생합니다.
        """
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")

        return self._seats[seat_id]
