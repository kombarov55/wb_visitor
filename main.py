import os

import scheduler
from config import database
from repository import task_repository, phone_number_repository


def create_missing_dirs():
    if not os.path.exists("screenshots"):
        print("creating dir screenshots/")
        os.makedirs("./screenshots", exist_ok=True)


if __name__ == '__main__':
    create_missing_dirs()

    database.base.metadata.create_all(bind=database.engine)
    task_repository.set_all_running_to_failed()
    phone_number_repository.set_all_activating_to_just_received()
    scheduler.run()
