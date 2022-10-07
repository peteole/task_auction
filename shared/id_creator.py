import uuid


def create_id() -> str:
    return str(uuid.uuid1())
