from datetime import datetime, timedelta, timezone

from src import config


def is_quiet_time(now: datetime | None = None) -> bool:
    """True, если сейчас ночная пауза. Работает и для окна через полночь (например, 22-06)."""
    tz = timezone(timedelta(hours=config.TIMEZONE_OFFSET_HOURS))
    hour = (now or datetime.now(tz)).astimezone(tz).hour
    start, end = config.QUIET_START_HOUR, config.QUIET_END_HOUR
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end
