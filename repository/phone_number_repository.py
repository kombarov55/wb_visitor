from sqlalchemy.orm import Session
from sqlalchemy import text

from config import database
from model.phone_number import PhoneNumberVO, PhoneNumberStatus
from model.task import TaskVO


def find_by_id(session: Session, id: int):
    return session.query(PhoneNumberVO).filter(PhoneNumberVO.id == id).first()


def find_just_received(session: Session):
    return session.query(PhoneNumberVO)\
        .filter(PhoneNumberVO.status == PhoneNumberStatus.just_received)\
        .all()


def count_activating():
    with database.engine.connect() as con:
        rows = con.execute(text("select count(*) from phone_number where status = 'ACTIVATING'"))
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return int(result[0])


def update(session: Session, vo: PhoneNumberVO):
    v = session.query(PhoneNumberVO).filter(PhoneNumberVO.id == vo.id).first()
    v.ext_id = vo.ext_id
    v.number = vo.number
    v.cookies_json = vo.cookies_json
    v.status = vo.status
    v.status_change_datetime = vo.status_change_datetime

    session.add(v)
    session.commit()
    session.refresh(v)
    return v


def get_number_for_task(task: TaskVO):
    sql = """
select pn.id, ext_id, number, cookies_json, status
from phone_number pn
where pn.status = 'ACTIVATED'
  and pn.number not in (select t.number_used
                        from task t
                        where t.task_request_id = {} and t.article like '{}' and t.number_used is not null)
limit 1
    """.format(task.task_request_id, task.article)
    with database.engine.connect() as con:
        rows = con.execute(text(sql))
        return extract_single_number(rows)


def get_any_number():
    with database.engine.connect() as con:
        rows = con.execute(text("""
select pn.id, ext_id, number, cookies_json, status
from phone_number pn
where pn.status = 'ACTIVATED'
limit 1        
        """))
        return extract_single_number(rows)


def extract_single_number(rows):
    result = []

    for row in rows:
        vo = PhoneNumberVO(
            id=row[0],
            ext_id=row[1],
            number=row[2],
            cookies_json=row[3],
            status=row[4]
        )
        result.append(vo)
    if len(result) == 0:
        return None
    else:
        return result[0]


def set_status(session: Session, id: int, status: str):
    vo = find_by_id(session, id)
    vo.status = status
    session.add(vo)
    session.commit()


def set_all_activating_to_just_received():
    with database.engine.connect() as con:
        con.execute(text("update phone_number set status='JUST_RECEIVED' where status = 'ACTIVATING'"))
