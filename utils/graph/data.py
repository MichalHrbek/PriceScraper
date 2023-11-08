db: dict[str,list[dict]] = {}

def set(data):
    global db
    db = data

def get():
    return db