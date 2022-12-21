from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from config import database, app_config
from model.proxy import ProxyVO


def get_all(session: Session, offset: int, limit: int):
    return session.query(ProxyVO).all()


def save(session: Session, x: dict):
    vo = ProxyVO(
        ip=x["ip"],
        username=x["username"],
        password=x["password"],
        created_datetime=datetime.now()
    )

    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def set_auth_blocked_datetime(id: int):
    with database.engine.connect() as con:
        con.execute("update proxy set auth_blocked_datetime = now() where id = {}".format(id))


def get_random_proxy():
    with database.engine.connect() as con:
        rows = con.execute("""select id, ip, username, password from proxy """)
        result = []
        for row in rows:
            result.append(ProxyVO(
                id=row[0],
                ip=row[1],
                username=row[2],
                password=row[3]
            ))
        hours = app_config.time_to_retry_in_hours_when_proxy_is_blocked
        for vo in result:
            if vo.auth_blocked_datetime is None:
                return vo
            if vo.auth_blocked_datetime + timedelta(hours=hours) < datetime.now():
                return vo
        return result[0]


def delete(id: int):
    with database.engine.connect() as con:
        con.execute("delete from proxy where id={}".format(id))
