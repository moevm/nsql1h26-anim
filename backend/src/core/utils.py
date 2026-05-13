from datetime import datetime, timezone
from uuid import uuid4

def get_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_uid() -> str:
    return str(uuid4())