import datetime
from home.apps.config.encryption import secret_code
from hashlib import sha256


def encrypt():
    now = datetime.datetime.now()
    code = secret_code.format(str(now.hour), str(now.day), str(now.year), str(now.month))
    code = sha256(code.encode()).hexdigest()
    return code