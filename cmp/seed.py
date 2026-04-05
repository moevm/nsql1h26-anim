from faker import Faker
from uuid import uuid4
from datetime import datetime, timezone
import random

faker = Faker()

def seed_users(count):
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


def seed_posts(count):
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


def seed_tags(count):
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


def seed_animals(count):
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


def seed_categories(count):
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


def seed_follows(users):
    """User -[:FOLLOWS]-> User"""
    pairs = set()
    follows = []
    user_ids = [u['id'] for u in users]

    for user in users:
        # each user follows 1..3 random others
        targets = random.sample([uid for uid in user_ids if uid != user['id']],
                                k=min(3, len(user_ids) - 1))
        for target_id in targets:
            pair = (user['id'], target_id)
            if pair not in pairs:
                pairs.add(pair)
                follows.append({
                    'follower_id': user['id'],
                    'followee_id': target_id,
                    'created_at': faker.date_this_decade().isoformat(),
                })

    query = """
    UNWIND $follows AS f
    MATCH (follower:User {id: f.follower_id})
    MATCH (followee:User {id: f.followee_id})
    CREATE (follower)-[:FOLLOWS {created_at: f.created_at}]->(followee)
    """
    return follows, query


def seed_authored(users, posts):
    """User -[:AUTHORED]-> Post  (one author per post)"""
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


def seed_likes(users, posts):
    """User -[:LIKES]-> Post"""
    pairs = set()
    likes = []

    for user in users:
        liked_posts = random.sample(posts, k=min(5, len(posts)))
        for post in liked_posts:
            pair = (user['id'], post['id'])
            if pair not in pairs:
                pairs.add(pair)
                likes.append({
                    'user_id': user['id'],
                    'post_id': post['id'],
                    'created_at': faker.date_this_decade().isoformat(),
                })

    query = """
    UNWIND $likes AS l
    MATCH (u:User {id: l.user_id})
    MATCH (p:Post {id: l.post_id})
    CREATE (u)-[:LIKES {created_at: l.created_at}]->(p)
    """
    return likes, query


def seed_has_tag(posts, tags):
    """Post -[:HAS_TAG]-> Tag"""
    pairs = set()
    has_tags = []

    for post in posts:
        chosen_tags = random.sample(tags, k=min(3, len(tags)))
        for tag in chosen_tags:
            pair = (post['id'], tag['id'])
            if pair not in pairs:
                pairs.add(pair)
                has_tags.append({
                    'post_id': post['id'],
                    'tag_id': tag['id'],
                })

    query = """
    UNWIND $has_tags AS ht
    MATCH (p:Post {id: ht.post_id})
    MATCH (t:Tag  {id: ht.tag_id})
    CREATE (p)-[:HAS_TAG]->(t)
    """
    return has_tags, query


def seed_observed(posts, animals):
    """Post -[:OBSERVED]-> Animal"""
    pairs = set()
    observed = []

    for post in posts:
        chosen = random.sample(animals, k=min(2, len(animals)))
        for animal in chosen:
            pair = (post['id'], animal['id'])
            if pair not in pairs:
                pairs.add(pair)
                observed.append({
                    'post_id': post['id'],
                    'animal_id': animal['id'],
                })

    query = """
    UNWIND $observed AS o
    MATCH (p:Post   {id: o.post_id})
    MATCH (a:Animal {id: o.animal_id})
    CREATE (p)-[:OBSERVED]->(a)
    """
    return observed, query


def seed_belongs_to(animals, categories):
    """Animal -[:BELONGS_TO]-> Category"""
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
