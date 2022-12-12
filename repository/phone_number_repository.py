from sqlalchemy.orm import Session

from model.phone_number import PhoneNumberVO, PhoneNumberStatus


def find_just_received(session: Session):
    return session.query(PhoneNumberVO)\
        .filter(PhoneNumberVO.status == PhoneNumberStatus.just_received)\
        .all()


def update(session: Session, vo: PhoneNumberVO):
    v = session.query(PhoneNumberVO).filter(PhoneNumberVO.id == vo.id).first()
    v.ext_id = vo.ext_id
    v.number = vo.number
    v.cookies_json = vo.cookies_json
    v.status = vo.status

    session.add(v)
    session.commit()
    session.refresh(v)
    return v
