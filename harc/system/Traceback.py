import sys
import traceback


class Traceback:
    def __init__(self):
        pass

    @staticmethod
    def build():
        code, message, backtrace = sys.exc_info()
        format_backtrace = "".join(traceback.format_exception(code, message, backtrace))
        return {"code": repr(code), "message": repr(message), "backtrace": repr(format_backtrace)}
