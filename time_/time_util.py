import time
import pytz
import datetime

"""
time.time() : (Uni) utc timestamp
time.gmtime(): time.struct_time  # UTC
time.localtime(): time.struct_time  # 서버 시간
time.mktime()  # use timezone
time.ctime(secs) == time.asctime(time.localtime(secs)) # use timezone
"""

UTC = pytz.UTC
KOR = pytz.timezone('Etc/GMT-9')


def utc_to_kor(dt):
    # UTC 시간을 KOR 기준으로 바꿔준다. tzinfo 는 제거한다.
    return UTC.localize(dt).astimezone(KOR).replace(tzinfo=None)


def kst_dt_now():
    utc_dt = datetime.datetime.utcnow()
    kst_dt = utc_to_kor(utc_dt)
    return kst_dt


def kst_today():
    dt = kst_dt_now()
    return dt.date()


# FIXME
def utc_to_kor_ts(dt):
    # TODO mktime 은 서버 시간을 기준으로 바꿔준다.
    dt = utc_to_kor(dt)
    return time.mktime(dt.timetuple())


# FIXME
def kor_ts_to_utc(ts):
    # TODO fromtimestamp 는 서버 시간을 기준으로 바꿔준다.
    return datetime.datetime.fromtimestamp(ts) \
        .replace(tzinfo=KOR) \
        .astimezone(UTC) \
        .replace(tzinfo=None)


def n_days_later(dt=None, n=None):
    if dt:
        return dt + datetime.timedelta(days=n)
    else:
        return kst_dt_now() + datetime.timedelta(days=n)


def n_hours_later(dt=None, n=None):
    if dt:
        return dt + datetime.timedelta(hours=n)
    else:
        return kst_dt_now() + datetime.timedelta(hours=n)


def n_sec_later(dt=None, n=None):
    if dt:
        return dt + datetime.timedelta(seconds=n)
    else:
        return kst_dt_now() + datetime.timedelta(seconds=n)


def in_n_days(dt, n, crt=None):
    """ crt - n(days) < dt < crt """
    if not crt:
        crt = kst_dt_now()
    return dt >= n_days_later(crt, -1 * n)


def refine_dt(dt, hour=False, minute=True, second=True):
    """ True : 해당 값 지워버림 """
    if hour:
        dt = dt.replace(hour=0)
    if minute:
        dt = dt.replace(minute=0)
    if second:
        dt = dt.replace(second=0, microsecond=0)
    return dt


formatter = [
    # 과거, 미래
    ['방금', '곧'],  # 10s
    ['{}초 전', '{}초 후'],  # 60
    ['{}분 전', '{}분 후'],  # 60 ~ 3600
    ['{}시간 전', '{}시간 후'],  # 3600 ~ 3600 * 24
    ['{}일 전', '{}일 후'],  # 3600 * 24 ~
    # ['{}주일 전', '{}주일 후'],
    # ['1개월 전', '1개월 후'],
    # ['{}개월 전', '{}개월 후'],
    # ['1년 전', '1년 후'],
    # ['{}년 전', '{}년 후']
]


def _time_ago_format(diff_sec, is_past):
    criteria = [10, 60, 3600, 3600 * 24]
    divide_by = [1, 1, 60, 3600, 3600 * 24]

    diff_sec = abs(diff_sec)
    for idx, value in enumerate(criteria):
        if diff_sec < value:
            return formatter[idx][is_past].format(int(diff_sec / divide_by[idx]))
    return formatter[-1][is_past].format(int(diff_sec / divide_by[-1]))


def calc_diff_sec(dt, crt=None):
    if not crt:
        crt = kst_dt_now()
    diff = crt - dt
    return diff.total_seconds()


def time_ago(dt, from_=None):
    """ from_ - dt 로 """
    if type(dt) != datetime.datetime:
        if type(dt) == datetime.date:
            dt = datetime.datetime.fromordinal(dt.toordinal())
        else:
            raise TypeError('Invalid Type.')
    if not from_:
        from_ = kst_dt_now()
    diff = calc_diff_sec(dt, from_)
    is_past = int(diff < 0)  # 0: 과거, 1: 미래
    return _time_ago_format(diff, is_past)


def day_ago(dt, crt=None):
    """ N일 M시간 차이 -> return N """
    if not crt:
        crt = kst_dt_now()
    diff = calc_diff_sec(dt, crt)
    diff_day = int(diff / (3600 * 24))
    return diff_day
