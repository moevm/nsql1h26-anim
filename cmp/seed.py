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


def seed_users_sql(count=10000):
    users = [
        {
            'id': str(uuid4()),
            'locationId': faker.city(),
            'email': faker.email(),
            'password': faker.password(),
            'username': faker.user_name(),
            'role': random.choice(['user', 'admin', 'moderator']),
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO users (id, locationId, email, password, username, role, first_name, last_name, timestamp, created_at)
        VALUES (%(id)s, %(locationId)s, %(email)s, %(password)s, %(username)s, %(role)s, %(first_name)s, %(last_name)s, %(timestamp)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return users, query


def seed_posts_sql(count=5000):
    statuses = ['published', 'draft', 'archived']
    posts = [
        {
            'id': str(uuid4()),
            'title': faker.sentence(),
            'text': faker.text(max_nb_chars=500),
            'content': faker.text(max_nb_chars=1000),
            'image_url': faker.image_url(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO posts (id, title, text, content, image_url, timestamp, created_at)
        VALUES (%(id)s, %(title)s, %(text)s, %(content)s, %(image_url)s, %(timestamp)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return posts, query


def seed_tags_sql(count=200):
    tags = [
        {
            'tagId': str(uuid4()),
            'name': faker.unique.word(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO tags (tagId, name, created_at)
        VALUES (%(tagId)s, %(name)s, %(created_at)s)
        ON CONFLICT (tagId) DO NOTHING
    """
    return tags, query


def seed_animals_sql(count=500):
    species_list = ['Panthera leo', 'Elephas maximus', 'Tursiops truncatus',
                    'Gorilla gorilla', 'Ailuropoda melanoleuca', 'Canis lupus',
                    'Felis catus', 'Canis familiaris', 'Equus ferus', 'Bos taurus']
    habitats = ['forest', 'ocean', 'desert', 'grassland', 'tundra', 'wetland', 'mountain', 'savanna']

    animals = [
        {
            'id': str(uuid4()),
            'taxonId': str(uuid4()),
            'species': random.choice(species_list),
            'habitat': random.choice(habitats),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO animals (id, taxonId, species, habitat, created_at)
        VALUES (%(id)s, %(taxonId)s, %(species)s, %(habitat)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return animals, query


def seed_categories_sql(count=30):
    classes = ['Mammalia', 'Aves', 'Reptilia', 'Amphibia', 'Actinopterygii', 'Insecta', 'Arachnida']
    habitats = ['forest', 'ocean', 'desert', 'grassland', 'tundra', 'wetland', 'mountain']

    categories = [
        {
            'id': str(uuid4()),
            'class': random.choice(classes),
            'habitat': random.choice(habitats),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO categories (id, class, habitat, created_at)
        VALUES (%(id)s, %(class)s, %(habitat)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return categories, query


def seed_locations_sql(users, count=1000):
    user_ids = [u['id'] for u in users]
    locations = [
        {
            'id': str(uuid4()),
            'userid': random.choice(user_ids),
            'name': faker.city(),
            'coordinates': f'({random.uniform(-90, 90)}, {random.uniform(-180, 180)})',
            'rank': random.randint(1, 10),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(min(count, len(user_ids)))
    ]
    query = """
        INSERT INTO locations (id, userid, name, coordinates, rank, created_at)
        VALUES (%(id)s, %(userid)s, %(name)s, %(coordinates)s, %(rank)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return locations, query


def seed_posts_content_sql(count=5000):
    posts = [
        {
            'id': str(uuid4()),
            'title': faker.sentence(),
            'text': faker.text(max_nb_chars=500),
            'content': faker.text(max_nb_chars=1000),
            'image_url': faker.image_url(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for _ in range(count)
    ]
    query = """
        INSERT INTO posts_content (id, title, text, content, image_url, timestamp, created_at)
        VALUES (%(id)s, %(title)s, %(text)s, %(content)s, %(image_url)s, %(timestamp)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return posts, query


def seed_follows_sql(users, count=500):
    user_ids = [u['id'] for u in users]
    follows = [
        {
            'followerId': a,  # кто подписывается
            'timestamp': faker.date_this_decade().isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for a, _ in _unique_pairs(user_ids, user_ids, count, same=True)
    ]
    query = """
        INSERT INTO followers (followerId, timestamp, created_at)
        VALUES (%(followerId)s, %(timestamp)s, %(created_at)s)
    """
    return follows, query


def seed_authored_sql(users, posts):
    authored = [
        {
            'user_id': random.choice(users)['id'],
            'post_id': post['id'],
        }
        for post in posts
    ]
    query = """
        UPDATE posts 
        SET userid = %(user_id)s 
        WHERE id = %(post_id)s
    """
    return authored, query


def seed_likes_sql(users, posts, count=200):
    user_ids = [u['id'] for u in users]
    post_ids = [p['id'] for p in posts]

    likes = [
        {
            'userid': a,
            'timestamp': faker.date_this_year().isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        for a, _ in _unique_pairs(user_ids, post_ids, count)
    ]
    query = """
        INSERT INTO likes (userid, timestamp, created_at)
        VALUES (%(userid)s, %(timestamp)s, %(created_at)s)
    """
    return likes, query


def seed_comments_sql(users, posts, count=1000):
    user_ids = [u['id'] for u in users]
    post_ids = [p['id'] for p in posts]

    comments = []
    for i in range(count):
        comment = {
            'id': str(uuid4()),
            'userid': random.choice(user_ids),
            'commentId': None,
            'timestamp': faker.date_this_year().isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        comments.append(comment)

    for i in range(min(count // 10, len(comments))):
        if i > 0:
            parent = random.choice(comments[:i])
            comments[i]['commentId'] = parent['id']

    query = """
        INSERT INTO comments (id, userid, commentId, timestamp, created_at)
        VALUES (%(id)s, %(userid)s, %(commentId)s, %(timestamp)s, %(created_at)s)
        ON CONFLICT (id) DO NOTHING
    """
    return comments, query


def seed_has_tag_sql(posts, tags, count=250):
    post_ids = [p['id'] for p in posts]
    tag_ids = [t['tagId'] for t in tags]

    has_tags = [
        {
            'postId': a,
            'tagId': b,
        }
        for a, b in _unique_pairs(post_ids, tag_ids, count)
    ]
    query = """
        INSERT INTO post_tags (postId, tagId)
        VALUES (%(postId)s, %(tagId)s)
        ON CONFLICT (postId, tagId) DO NOTHING
    """
    return has_tags, query


def seed_observed_sql(posts, animals, count=150):
    post_ids = [p['id'] for p in posts]
    animal_ids = [a['id'] for a in animals]

    observed = [
        {
            'postId': a,
            'animalId': b,
        }
        for a, b in _unique_pairs(post_ids, animal_ids, count)
    ]
    query = """
        INSERT INTO post_animals (postId, animalId)
        VALUES (%(postId)s, %(animalId)s)
        ON CONFLICT (postId, animalId) DO NOTHING
    """
    return observed, query


def seed_belongs_to_sql(animals, categories):
    belongs = [
        {
            'animalId': animal['id'],
            'categoryId': random.choice(categories)['id'],
        }
        for animal in animals
    ]
    query = """
        INSERT INTO animal_categories (animalId, categoryId)
        VALUES (%(animalId)s, %(categoryId)s)
        ON CONFLICT (animalId, categoryId) DO NOTHING
    """
    return belongs, query


def get_truncate_order():
    return [
        'post_tags',
        'post_animals',
        'animal_categories',
        'followers',
        'comments',
        'likes',
        'posts',
        'posts_content',
        'locations',
        'animals',
        'categories',
        'tags',
        'users'
    ]