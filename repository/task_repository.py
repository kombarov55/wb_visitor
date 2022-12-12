from sqlalchemy.orm import Session

from model.task import TaskVO


def find_by_id(session: Session, id: int):
    return session.query(TaskVO).filter(TaskVO.id == id).first()