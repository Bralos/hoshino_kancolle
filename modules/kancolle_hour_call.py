import pytz
from datetime import datetime
import kokkoro
from kokkoro.service import Service, BroadcastTag, BroadcastService

sv = Service('hourcall', enable_on_default=True, help_='时报')
svhc = BroadcastService('kancolle_hour_call',
    broadcast_tag=[BroadcastTag.default], enable_on_default=False, help_='舰C时报')
tz = pytz.timezone('America/New_York')

def get_hour_call():
    """挑出一组时报，每日更换，一日之内保持相同"""
    cfg = kokkoro.config.modules.kancolle_hour_call
    now = datetime.now(tz)
    hc_groups = cfg.HOUR_CALLS_ON
    g = hc_groups[ now.day % len(hc_groups) ]
    return cfg.HOUR_CALLS[g]


@svhc.scheduled_job('cron', hour='*', minute="*")
async def hour_call():
    now = datetime.now(tz)
    if 4 <= now.hour <= 8:
        return  # 宵禁 免打扰
    msg = get_hour_call()[now.hour]
    await svhc.broadcast(msg)
    #发送语音

@sv.on_prefix('手动报时')
async def manual_hour_call(bot,ev):
    now = datetime.now(tz)
    msg = get_hour_call()[now.hour]
    await bot.kkr_send(ev,msg)
    #发送语音
