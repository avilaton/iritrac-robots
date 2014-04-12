import sys
from time import sleep
from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def some_job():
    print "Decorated job"

sched.start()

while True:
	sleep(1)
	sys.stdout.write('.'); sys.stdout.flush()
	pass