import time
from concurrent.futures import ThreadPoolExecutor

from config import app_config
from scheduled import activate_numbers_service, task_service


def run():
    with ThreadPoolExecutor(app_config.max_workers) as executor:
        while True:
            activate_numbers_service.tick(executor)
            task_service.tick(executor)

            time.sleep(app_config.schedule_sleep_time_in_seconds)
