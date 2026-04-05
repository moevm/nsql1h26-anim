import psycopg2
from faker import Faker


class PostgresConnection:
    def __init__(self, host, port, user, password):
        self.conn = psycopg2.connect(host=host, port=port, user=user, password=password)
        self.faker = Faker()
    
    def seed(self):
        def seed_users(count, batch_size):
            user = [{
                'id': str(uuid4()),
                'email': self.fake.email(),
                'password': self.fake.password(),
                'username': self.fake.user_name(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'bio': self.fake.text(max_nb_chars=500),
                'avatar_url': self.fake.image_url(),
                'role': 'user',
                'created_at': datetime.now(timezone.utc).isoformat()
            } for _ in range(count) ]

        for i in range(0, count, batch_size):
            batch = users[i:i + batch_size]
            self.conn.run(query, users=batch)