from faker import Faker
from uuid import uuid4
from datetime import datetime, timezone
import random

faker = Faker()


def seed_users(count=10000):
    users = [
        {
            'id': str(uuid4()),
            'email': faker.email(),
            'password': faker.password(),
            'username': faker.user_name(),
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'bio': faker.text(max_nb_chars=500),
            'avatar_url': faker.image_url(),
            'role': 'user',
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
    UNWIND $users AS users
    CREATE (u:User)
    SET u = users
    """
    return users, query


def seed_posts(count=5000):
    statuses = ['published', 'draft', 'archived']
    posts = [
        {
            'id': str(uuid4()),
            'description': faker.text(max_nb_chars=300),
            'photo_url': faker.image_url(),
            'location': faker.city(),
            'status': random.choice(statuses),
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
    UNWIND $posts AS posts
    CREATE (p:Post)
    SET p = posts
    """
    return posts, query


def seed_tags(count=200):
    tags = [
        {
            'id': str(uuid4()),
            'name': faker.word(),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
    UNWIND $tags AS tags
    MERGE (t:Tag {name: tags.name})
    SET t = tags
    """
    return tags, query


def seed_animals(count=500):
    species_list = ['Panthera leo', 'Elephas maximus', 'Tursiops truncatus',
                    'Gorilla gorilla', 'Ailuropoda melanoleuca', 'Canis lupus']
    animals = [
        {
            'id': str(uuid4()),
            'name': faker.first_name(),
            'species': random.choice(species_list),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
    UNWIND $animals AS animals
    CREATE (a:Animal)
    SET a = animals
    """
    return animals, query


def seed_categories(count=30):
    classes = ['Mammalia', 'Aves', 'Reptilia', 'Amphibia', 'Actinopterygii']
    habitats = ['forest', 'ocean', 'desert', 'grassland', 'tundra', 'wetland']
    categories = [
        {
            'id': str(uuid4()),
            'class': random.choice(classes),
            'habitat': random.choice(habitats),
        }
        for _ in range(count)
    ]
    query = """
    UNWIND $categories AS categories
    CREATE (c:Category)
    SET c = categories
    """
    return categories, query


def _unique_pairs(a_ids, b_ids, count, same=False):
    max_pairs = len(a_ids) * len(b_ids) - (len(a_ids) if same else 0)
    count = min(count, max_pairs)
    pairs = set()
    while len(pairs) < count:
        a = random.choice(a_ids)
        b = random.choice(b_ids)
        if same and a == b:
            continue
        pairs.add((a, b))
    return list(pairs)


def seed_follows(users, count=500000):
    user_ids = [u['id'] for u in users]
    follows = [
        {
            'follower_id': a,
            'followee_id': b,
            'created_at': faker.date_this_decade().isoformat(),
        }
        for a, b in _unique_pairs(user_ids, user_ids, count, same=True)
    ]
    query = """
    UNWIND $follows AS f
    MATCH (follower:User {id: f.follower_id})
    MATCH (followee:User {id: f.followee_id})
    CREATE (follower)-[:FOLLOWS {created_at: f.created_at}]->(followee)
    """
    return follows, query


def seed_authored(users, posts):
    authored = [
        {
            'user_id': random.choice(users)['id'],
            'post_id': post['id'],
        }
        for post in posts
    ]
    query = """
    UNWIND $authored AS a
    MATCH (u:User {id: a.user_id})
    MATCH (p:Post {id: a.post_id})
    CREATE (u)-[:AUTHORED]->(p)
    """
    return authored, query


def seed_likes(users, posts, count=200000):
    user_ids = [u['id'] for u in users]
    post_ids = [p['id'] for p in posts]
    likes = [
        {
            'user_id': a,
            'post_id': b,
            'created_at': faker.date_this_decade().isoformat(),
        }
        for a, b in _unique_pairs(user_ids, post_ids, count)
    ]
    query = """
    UNWIND $likes AS l
    MATCH (u:User {id: l.user_id})
    MATCH (p:Post {id: l.post_id})
    CREATE (u)-[:LIKES {created_at: l.created_at}]->(p)
    """
    return likes, query


def seed_has_tag(posts, tags, count=25000):
    post_ids = [p['id'] for p in posts]
    tag_ids  = [t['id'] for t in tags]
    has_tags = [
        {'post_id': a, 'tag_id': b}
        for a, b in _unique_pairs(post_ids, tag_ids, count)
    ]
    query = """
    UNWIND $has_tags AS ht
    MATCH (p:Post {id: ht.post_id})
    MATCH (t:Tag  {id: ht.tag_id})
    CREATE (p)-[:HAS_TAG]->(t)
    """
    return has_tags, query


def seed_observed(posts, animals, count=15000):
    post_ids   = [p['id'] for p in posts]
    animal_ids = [a['id'] for a in animals]
    observed = [
        {'post_id': a, 'animal_id': b}
        for a, b in _unique_pairs(post_ids, animal_ids, count)
    ]
    query = """
    UNWIND $observed AS o
    MATCH (p:Post   {id: o.post_id})
    MATCH (a:Animal {id: o.animal_id})
    CREATE (p)-[:OBSERVED]->(a)
    """
    return observed, query


def seed_belongs_to(animals, categories):
    belongs = [
        {
            'animal_id': animal['id'],
            'category_id': random.choice(categories)['id'],
        }
        for animal in animals
    ]
    query = """
    UNWIND $belongs AS b
    MATCH (a:Animal   {id: b.animal_id})
    MATCH (c:Category {id: b.category_id})
    CREATE (a)-[:BELONGS_TO]->(c)
    """
    return belongs, query