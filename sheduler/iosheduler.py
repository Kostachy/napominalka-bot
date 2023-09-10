# import json
#
# from apscheduler_di import ContextSchedulerDecorator

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from apscheduler.jobstores.redis import RedisJobStore

# from config.bot_config import config

# redis storage not working

# job_stores = {
#     "default": RedisJobStore(jobs_key="dispatched_trips_jobs",
#                              run_times_key="dispatched_trips_running",
#                              host=config.redis_db.redis_host,
#                              port=config.redis_db.redis_port,
#                              password=config.redis_db.redis_pass,
#                              )
# }

sched = AsyncIOScheduler()