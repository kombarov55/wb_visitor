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


class TaskStatus:
    scheduled = "SCHEDULED"
    running = "RUNNING"
    no_available_numbers = "NO_AVAILABLE_NUMBERS"
    success = "SUCCESS"
    failed = "FAILED"


class ActionType:
    add_report = "Пожаловаться на отзыв"
    add_question = "Задать вопрос"
    add_comparison_question = "Задать вопрос со сравнением"
    add_to_cart = "Добавить в корзину"
    add_to_cart_and_remove = "Добавить и убрать из корзины"
    remove_from_cart = "Убрать из корзины"
    add_to_favorites = "Добавить в избранное"
    add_to_favorites_and_remove = "Добавить и убрать из избранного"
    remove_from_favorites = "Убрать из избранного"
