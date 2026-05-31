from seat_reservation_system.seat_store import SeatStore


def test_reserve_and_cancel_flow():
    store = SeatStore([1, 2])
    seat_id, name = store.reserve(1, "Alex")
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.status(1)
    assert (seat_id, name) == (1, "Alex")

    seat_id, name = store.cancel(1, "Alex")
    assert (seat_id, name) == (1, None)


def test_stats_counts_reserved_and_available():
    store = SeatStore([1, 2, 3])
    store.reserve(2, "Mina")
    assert store.stats() == {"total": 3, "reserved": 1, "available": 2}
