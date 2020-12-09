from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler(timezone="Etc/UTC")
from tzlocal import get_localzone
tz = get_localzone()
print(tz)
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=6,minute=50)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
