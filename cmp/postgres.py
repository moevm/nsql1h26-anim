import psycopg2
from uuid import uuid4
from datetime import datetime, timezone
from faker import Faker


class PostgresConnection:
    def __init__(self, host, port, user, password):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password)
    
    def seed(self):