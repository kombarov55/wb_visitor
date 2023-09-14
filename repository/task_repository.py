from sqlalchemy.orm import Session
from sqlalchemy import text

from config import database
from model.task import TaskVO


def find_by_id(session: Session, id: int):
    return session.query(TaskVO).filter(TaskVO.id == id).first()


def update(session: Session, vo: TaskVO):
    v = find_by_id(session, vo.id)
    v.status = vo.status
    v.end_datetime = vo.end_datetime
    v.number_used = vo.number_used
    session.add(v)
    session.commit()


def set_all_running_to_failed():
    with database.engine.connect() as con:
        con.execute(text("update task set status = 'FAILED' where status = 'RUNNING'"))
 

def count_running_tasks():
    with database.engine.connect() as con:
        rows = con.execute(text("select count(*) from task where status = 'RUNNING'"))
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return result[0]


def set_finished_status_if_group_is_ready(task_id):
    print("set finished status if group is reqady")

    task_group_id = get_task_group_id(task_id)
    print("task_group_id = {}".format(task_group_id))

    count = count_scheduled_tasks(task_group_id)
    print("found {} scheduled tasks".format(int(count)))

    if count == 0:
        print("setting status 'SUCCESS' for task_group_id={}".format(task_group_id))
        set_success_status_to_task_group_by_task_id(task_group_id)
        print("success")


def count_scheduled_tasks(task_request_id):
    with database.engine.connect() as con:
        rows = con.execute(text("""
            select count(*)
            from task
            where status = 'SCHEDULED'
            and task_request_id = {}
        """.format(str(task_request_id))))
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return int(result[0])


def get_task_group_id(task_id):
    with database.engine.connect() as con:
        rows = con.execute(text("""
            select task_request_id
            from task
            where id = {}
            """.format(str(task_id))))
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return int(result[0])


def set_success_status_to_task_group_by_task_id(task_group_id):
    with database.engine.connect() as con:
        con.execute(text("""
        update task_request
        set status = 'SUCCESS'
        where id = {}""".format(str(task_group_id))))
