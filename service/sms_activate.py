import time

from playwright.sync_api import Page
from smsactivate.api import SMSActivateAPI

from config import app_config

sa = SMSActivateAPI(app_config.sms_activate_key)


def is_enough_money():
    s = sa.getBalance()["balance"]
    money = int(s)
    return money > 0


def receive_code(id: str):
    total_secs_spent = 0

    while True:
        rs = sa.getStatus(id=id)
        print(rs)

        received = type(rs) == str and rs.split(":")[0] == "STATUS_OK"

        if not received:
            print("sms is not received yet")
            time.sleep(3)
            total_secs_spent += 3
        else:
            code = rs.split(":")[1]
            print("sms received. code={}".format(code))

            return code

        if total_secs_spent > 60:
            return None


def is_code_received(id: str):
    rs = sa.getStatus(id=id)
    status = rs.split(":")[0]
    return status == "STATUS_OK"


if __name__ == "__main__":
    iid = "1178443173"

    print(sa.getStatus(iid))
    print(sa.setStatus(id="1178443173", status=6))
    print(sa.getStatus(iid))
