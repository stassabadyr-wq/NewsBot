from datetime import datetime, timedelta, timezone

from src.quiet import is_quiet_time

MSK = timezone(timedelta(hours=3))


def at(hour):
    return datetime(2026, 10, 22, hour, 30, tzinfo=MSK)


def test_quiet_hours():
    assert is_quiet_time(at(0))
    assert is_quiet_time(at(7))
    assert not is_quiet_time(at(8))
    assert not is_quiet_time(at(23))


def test_utc_time_is_converted():
    utc_2130 = datetime(2026, 10, 21, 21, 30, tzinfo=timezone.utc)  # 00:30 МСК
    assert is_quiet_time(utc_2130)
