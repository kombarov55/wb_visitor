from sqlalchemy.orm import Session

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
