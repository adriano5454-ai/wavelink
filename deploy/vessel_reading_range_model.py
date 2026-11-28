from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from .store import Problem


def limits(period='', start='', end='', *, today=None):
    today = today or datetime.now(timezone.utc).date()
    try:
        if period == 'custom':
            lower, upper = date.fromisoformat(start), date.fromisoformat(end)
            if (lower.isoformat(), upper.isoformat()) != (start, end):
                raise ValueError
        else:
            if start or end:
                raise ValueError
            months = {'': 1, '1': 1, '3': 3, '6': 6, '12': 12}[period]
            y, m = divmod(today.year * 12 + today.month - 1 - months, 12)
            lower, upper = date(y, m+1, min(today.day, monthrange(y,m+1)[1])), today
        if not date(1900,1,1) <= lower <= upper <= today or (upper-lower).days > 366:
            raise ValueError
    except (KeyError, TypeError, ValueError):
        raise Problem(422, 'Choose valid UTC dates up to 12 months, ending no later than today.')
    return lower.isoformat(), upper.isoformat(), (upper+timedelta(days=1)).isoformat()
