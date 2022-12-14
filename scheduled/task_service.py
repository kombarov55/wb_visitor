import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from playwright.sync_api import sync_playwright
from sqlalchemy.orm import Session

import playwright_util
from actions import set_like_to_comment, add_question, do_nothing, add_to_cart, remove_from_cart, add_to_favorites, \
    remove_from_favorites
from config import app_config, database
from model.phone_number import PhoneNumberVO
from model.task import TaskVO, TaskStatus, ActionType
from repository import task_repository, phone_number_repository


def tick(executor: ThreadPoolExecutor):
    session = database.session_local()

    tasks = find_tasks_ready_to_run(session)

    if len(tasks) != 0:
        print("found {} tasks to execute".format(len(tasks)))

    for task in tasks:
        executor.submit(process_task, task.id)
    session.close()


def find_tasks_ready_to_run(session: Session) -> list[TaskVO]:
    result = session.query(TaskVO).filter(TaskVO.status == TaskStatus.scheduled).filter(
        TaskVO.scheduled_datetime < datetime.now()).all()
    return result


def process_task(task_id: int):
    session = database.session_local()

    task = task_repository.find_by_id(session, task_id)

    if app_config.unique_numbers:
        phone_number = phone_number_repository.get_number_for_task(task)
    else:
        phone_number = phone_number_repository.get_any_number()

    if phone_number is None:
        print("no available numbers for task_request={}".format(task.task_request_id))
        task.status = TaskStatus.no_available_numbers
        task.end_datetime = datetime.now()
        task_repository.update(session, task)
        return

    task.status = TaskStatus.running
    task.number_used = phone_number.number
    task_repository.update(session, task)

    try:
        execute_task(task, phone_number)
        task.status = TaskStatus.success
        task.end_datetime = datetime.now()
        task_repository.update(session, task)
    except Exception as e:
        print(str(e))
        task.status = TaskStatus.failed
        task.error_msg = str(e)
        task.end_datetime = datetime.now()
        task_repository.update(session, task)

    session.close()


def execute_task(task: TaskVO, phone_number: PhoneNumberVO):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()

        playwright_util.set_cookies(page, phone_number.cookies_json)

        do_nothing.run(page)

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
        if task.action_type == ActionType.add_to_cart:
            url = "https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=XS".format(task.article)
            add_to_cart.run(page, url)
        if task.action_type == ActionType.remove_from_cart:
            remove_from_cart.run(page, task.article)
        if task.action_type == ActionType.add_to_favorites:
            url = "https://www.wildberries.ru/catalog/{}/detail.aspx?targetUrl=XS".format(task.article)
            add_to_favorites.run(page, url)
        if task.action_type == ActionType.remove_from_favorites:
            remove_from_favorites.run(page, task.article)
        return task
