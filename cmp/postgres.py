import psycopg2
from psycopg2.extras import execute_batch
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

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def query(self, query, batch=None):
        with self.conn:
            with self.conn.cursor() as cursor:
                if batch:
                    execute_batch(cursor, query, batch, page_size=1000)
                else:
                    cursor.execute(query)

                if cursor.description:
                    return cursor.fetchall()
    
    def create_table(self):
        queries = [
        """
        CREATE TABLE IF NOT EXISTS taxon (
            id UUID PRIMARY KEY,
            parent_id UUID REFERENCES taxon(id) ON DELETE SET NULL,
            name VARCHAR(255) NOT NULL,
            rank VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tag (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS "user" (
            id UUID PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(50),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            bio TEXT,
            avatar_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS animal (
            id UUID PRIMARY KEY,
            taxon_id UUID REFERENCES taxon(id) ON DELETE SET NULL,
            name VARCHAR(255),
            species VARCHAR(255),
            habitat VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS follower (
            follower_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            followed_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (follower_id, followed_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS post (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            animal_id UUID REFERENCES animal(id) ON DELETE SET NULL,
            location VARCHAR(255),
            title VARCHAR(255),
            content TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS post_tag (
            post_id UUID REFERENCES post(id) ON DELETE CASCADE,
            tag_id UUID REFERENCES tag(id) ON DELETE CASCADE,
            PRIMARY KEY (post_id, tag_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS post_like (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            post_id UUID REFERENCES post(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS comment (
            id UUID PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            post_id UUID REFERENCES post(id) ON DELETE CASCADE,
            parent_id UUID REFERENCES comment(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS comment_like (
            id SERIAL PRIMARY KEY,
            user_id UUID REFERENCES "user"(id) ON DELETE CASCADE,
            comment_id UUID REFERENCES comment(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        ]
        for q in queries:
            self.query(q)
    
    def create_index(self):
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_post_user_id ON post(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_comment_post_id ON comment(post_id)",
            "CREATE INDEX IF NOT EXISTS idx_post_like_user_id ON post_like(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_animal_taxon_id ON animal(taxon_id)",
            "CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name)"
        ]
        
        for index_query in indices:
            self.query(index_query)
    
    def seed(self, data):
        batch, q = seed_taxons_sql(data['taxon']);                  self.query(q, batch=batch)
        batch, q = seed_tags_sql(data['tag']);                      self.query(q, batch=batch)
        batch, q = seed_users_sql(data['user']);                    self.query(q, batch=batch)
        batch, q = seed_animals_sql(data['animal']);                self.query(q, batch=batch)
        batch, q = seed_posts_sql(data['post']);                    self.query(q, batch=batch)
        batch, q = seed_comments_sql(data['comment']);              self.query(q, batch=batch)
        batch, q = seed_post_tags_sql(data['post_tag']);            self.query(q, batch=batch)
        batch, q = seed_post_likes_sql(data['post_like']);          self.query(q, batch=batch)        
        batch, q = seed_comment_likes_sql(data['comment_like']);    self.query(q, batch=batch)
        batch, q = seed_followers_sql(data['follower']);            self.query(q, batch=batch)