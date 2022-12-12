import base64
import io

from PIL import Image
from smsactivate.api import SMSActivateAPI

from config import app_config

if __name__ == '__main__':
    sa = SMSActivateAPI(app_config.sms_activate_key)
    print(sa.getActiveActivations())
