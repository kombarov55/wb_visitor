import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from playwright.sync_api import sync_playwright
from sqlalchemy.orm import Session

import playwright_util
from actions import set_like_to_comment, add_question
from config import app_config, database
from model.task import TaskVO, TaskStatus, ActionType
from repository import task_repository


def run():
    with ThreadPoolExecutor(app_config.max_workers) as executor:
        while True:
            session = database.session_local()

            tasks = find_tasks_ready_to_run(session)

            for task in tasks:
                executor.submit(execute_task, task.id)
            session.commit()
            session.close()
            time.sleep(app_config.schedule_sleep_time_in_seconds)


def find_tasks_ready_to_run(session: Session) -> list[TaskVO]:
    result = session.query(TaskVO).filter(TaskVO.status == TaskStatus.scheduled).filter(
        TaskVO.scheduled_datetime < datetime.now()).all()
    print("found tasks to run: len={}".format(len(result)))
    return result


def process_task(task_id: int):
    session = database.session_local()

    task = task_repository.find_by_id(session, task_id)
    execute_task(task)
    task.status = TaskStatus.success
    task.end_datetime = datetime.now()

    session.add(task)
    session.commit()
    session.close()


def execute_task(task: TaskVO):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()
        playwright_util.load_cookies(page, "../cookies-auth.json")

        params = json.loads(task.params_json)
        if task.action_type == ActionType.set_like_to_comment:
            url = "https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=MI".format(task.article)
            name = params["name"]
            date = params["date"]
            set_like_to_comment.run(page, url, name, date, is_like=True)
        if task.action_type == ActionType.set_dislike_to_comment:
            url = "https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=MI".format(task.article)
            name = params["name"]
            date = params["date"]
            set_like_to_comment.run(page, url, name, date, is_like=False)
        if task.action_type == ActionType.add_question:
            url = "https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=MI".format(task.article)
            text_list = params["text_list"].split("\n")
            random_text = random.choice(text_list)
            add_question.run(page, url, random_text)
        return task

