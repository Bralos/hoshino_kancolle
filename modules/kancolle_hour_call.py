import pytz
from datetime import datetime
import kokkoro
from kokkoro.kokkoro import Service

sv = Service('hourcall', enable_on_default=False, help_='时报')
tz = pytz.timezone('America/New_York')

def get_hour_call():
    """挑出一组时报，每日更换，一日之内保持相同"""
    cfg = kokkoro.config.hourcall
    now = datetime.now(tz)
    hc_groups = cfg.HOUR_CALLS_ON
    g = hc_groups[ now.day % len(hc_groups) ]
    return cfg.HOUR_CALLS[g]


@sv.scheduled_job('cron', hour='*')
async def hour_call():
    now = datetime.now(tz)
    if 4 <= now.hour <= 8:
        return  # 宵禁 免打扰
    msg = get_hour_call()[now.hour]
    await sv.broadcast(msg, 'hourcall', 0)
    #发送语音

@sv.on_prefix('手动报时')
async def manual_hour_call():
    now = datetime.now(tz)
    msg = get_hour_call()[now.hour]
    await sv.broadcast(msg, 'hourcall', 0)
    #发送语音
