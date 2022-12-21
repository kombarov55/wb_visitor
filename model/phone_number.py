from sqlalchemy import Column, Integer, String, DateTime

from config import database


class PhoneNumberVO(database.base):
    __tablename__ = "phone_number"

    id = Column(Integer, primary_key=True, index=True)
    ext_id = Column(String)
    number = Column(String)
    cookies_json = Column(String)
    status = Column(String, index=True)
    received_datetime = Column(DateTime, index=True)
    status_change_datetime = Column(DateTime, index=True)


class PhoneNumberStatus:
    just_received = "JUST_RECEIVED"
    activating = "ACTIVATING"
    activated = "ACTIVATED"
    blocked = "BLOCKED"
