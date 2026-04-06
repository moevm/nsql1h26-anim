import psycopg2
from seed import *


class PostgresConnection:
    def __init__(self, host, user, password, port=5432):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname="postgres"
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def query(self, query, **kwargs):
        try:
            if kwargs and len(kwargs) == 1 and isinstance(list(kwargs.values())[0], list):
                param_name = list(kwargs.keys())[0]
                data_list = kwargs[param_name]

                if data_list:
                    for data in data_list:
                        self.cursor.execute(query, data)
            else:
                self.cursor.execute(query, kwargs)

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка выполнения запроса: {e}")
            raise

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                locationId VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                username VARCHAR(255) UNIQUE,
                role VARCHAR(50),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                timestamp TIMESTAMP,
                created_at TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS followers (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                followerId VARCHAR(255),
                timestamp TIMESTAMP,
                created_at TIMESTAMP,
                FOREIGN KEY (followerId) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                userid VARCHAR(255),
                title TEXT,
                text TEXT,
                content TEXT,
                image_url TEXT,
                timestamp TIMESTAMP,
                created_at TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                userid VARCHAR(255),
                commentId VARCHAR(255),
                timestamp TIMESTAMP,
                created_at TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (commentId) REFERENCES comments(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id SERIAL PRIMARY KEY,
                userid VARCHAR(255),
                timestamp TIMESTAMP,
                created_at TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts_content (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                userid VARCHAR(255),
                title TEXT,
                text TEXT,
                content TEXT,
                image_url TEXT,
                timestamp TIMESTAMP,
                created_at TIMESTAMP,
                FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                userid VARCHAR(255),
                name VARCHAR(255),
                coordinates POINT,
                rank INTEGER,
                FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                tagId VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                created_at TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_tags (
                postId VARCHAR(255),
                tagId VARCHAR(255),
                PRIMARY KEY (postId, tagId),
                FOREIGN KEY (postId) REFERENCES posts(id) ON DELETE CASCADE,
                FOREIGN KEY (tagId) REFERENCES tags(tagId) ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animals (
                uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                id VARCHAR(255) UNIQUE,
                taxonId VARCHAR(255),
                species VARCHAR(255),
                habitat VARCHAR(255),
                created_at TIMESTAMP
            )
        """)

        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_id ON users(id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_userid ON posts(userid)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_postid ON comments(id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_likes_userid ON likes(userid)")

        self.conn.commit()
        print("Все таблицы и связи успешно созданы")

    def seed(self):
        self.create_tables()

        tables_order = ['post_tags', 'followers', 'comments', 'likes', 'posts',
                        'posts_content', 'locations', 'animals', 'tags', 'users']

        for table in tables_order:
            try:
                self.cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
            except:
                pass
        self.conn.commit()

        users_data, users_query = seed_users_sql(10000)
        self.query(users_query, users=users_data)

        posts_data, posts_query = seed_posts_sql(5000)
        self.query(posts_query, posts=posts_data)

        tags_data, tags_query = seed_tags_sql(200)
        self.query(tags_query, tags=tags_data)

        animals_data, animals_query = seed_animals_sql(500)
        self.query(animals_query, animals=animals_data)

        categories_data, categories_query = seed_categories_sql(30)
        self.query(categories_query, categories=categories_data)

        follows_data, follows_query = seed_follows_sql(users_data, count=500)
        self.query(follows_query, follows=follows_data)

        authored_data, authored_query = seed_authored_sql(users_data, posts_data)
        self.query(authored_query, authored=authored_data)

        likes_data, likes_query = seed_likes_sql(users_data, posts_data, count=200)
        self.query(likes_query, likes=likes_data)

        has_tags_data, has_tags_query = seed_has_tag_sql(posts_data, tags_data, count=250)
        self.query(has_tags_query, has_tags=has_tags_data)

        observed_data, observed_query = seed_observed_sql(posts_data, animals_data, count=150)
        self.query(observed_query, observed=observed_data)

        belongs_data, belongs_query = seed_belongs_to_sql(animals_data, categories_data)
        self.query(belongs_query, belongs=belongs_data)