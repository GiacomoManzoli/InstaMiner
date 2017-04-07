from datetime import datetime

def current_timestamp():
    # type: () -> str
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
