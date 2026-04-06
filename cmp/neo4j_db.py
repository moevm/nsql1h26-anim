from neo4j import GraphDatabase
from seed import *

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    def query(self, query, **kwargs):
        with self.driver.session() as session:
            session.run(query, kwargs)

    def seed(self):
        users,      q = seed_users(10000);    self.query(q, users=users)
        posts,      q = seed_posts(5000);     self.query(q, posts=posts)
        tags,       q = seed_tags(200);       self.query(q, tags=tags)
        animals,    q = seed_animals(500);    self.query(q, animals=animals)
        categories, q = seed_categories(30);  self.query(q, categories=categories)

        follows,  q = seed_follows(users, count=500);            self.query(q, follows=follows)
        authored, q = seed_authored(users, posts);               self.query(q, authored=authored)
        likes,    q = seed_likes(users, posts, count=200);       self.query(q, likes=likes)
        has_tags, q = seed_has_tag(posts, tags, count=250);      self.query(q, has_tags=has_tags)
        observed, q = seed_observed(posts, animals, count=150);  self.query(q, observed=observed)
        belongs,  q = seed_belongs_to(animals, categories);      self.query(q, belongs=belongs)
