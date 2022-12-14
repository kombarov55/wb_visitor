from sqlalchemy import Column, Integer, String, DateTime

from config import database


class TaskVO(database.base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    task_request_id = Column(Integer)
    article = Column(String)
    action_type = Column(String)
    params_json = Column(String)
    scheduled_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    number_used = Column(String)
    status = Column(String)
    error_msg = Column(String)


class TaskStatus:
    scheduled = "SCHEDULED"
    running = "RUNNING"
    no_available_numbers = "NO_AVAILABLE_NUMBERS"
    success = "SUCCESS"
    failed = "FAILED"


class ActionType:
    add_question = "Задать вопрос"
    add_comparison_question = "Задать вопрос со сравнением"
    look_at_article = "Просмотр"
    set_like_to_comment = "Проставить лайк к комменту"
    set_dislike_to_comment = "Проставить дизлайк к комменту"
