import random
from uuid import uuid4
from faker import Faker

fake = Faker()

def generate_users(count):
    return [
        {
            'id': str(uuid4()),
            'email': fake.unique.email(),
            'username': fake.unique.user_name(),
            'password': fake.password(),
            'role': 'user',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'bio': fake.sentence(nb_words=10),
            'avatar_url': fake.image_url(),
            'created_at': fake.date_time_this_year().isoformat(),
            'location': fake.city()
        }
        for _ in range(count)
    ]

def generate_comments(count, user_ids, post_ids, reply_percent):
    comments = []
    for _ in range(count):
        comments.append({
            'id': str(uuid4()),
            'user_id': random.choice(user_ids),
            'post_id': random.choice(post_ids),
            'parent_id': None,
            'content': fake.text(max_nb_chars=200),
            'created_at': fake.date_time_this_year().isoformat(),
            'updated_at': fake.date_time_this_year().isoformat(),
        })
    reply_count = int(count * reply_percent)
    for _ in range(reply_count):
        parent = random.choice(comments)
        comments.append({
            'id': str(uuid4()),
            'user_id': random.choice(user_ids),
            'post_id': parent['post_id'],
            'parent_id': parent['id'],
            'content': fake.text(max_nb_chars=200),
            'created_at': fake.date_time_this_year().isoformat(),
            'updated_at': fake.date_time_this_year().isoformat(),
        })
    return comments

def generate_tags(count):
    return [
        {
            'id': str(uuid4()),
            'name': fake.unique.word()
        }
        for _ in range(count)
    ]

def generate_posts(count, user_ids, animal_ids):
    return [
        {
            'id': str(uuid4()),
            'user_id': random.choice(user_ids),
            'animal_id': random.choice(animal_ids),
            'title': fake.sentence(),
            'content': fake.paragraph(),
            'image_url': fake.image_url(),
            'location': fake.word(),
            'created_at': fake.date_time_this_year().isoformat(),
            'updated_at': fake.date_time_this_year().isoformat()
        }
        for _ in range(count)
    ]

def generate_taxons(count):
    taxons = []
    ranks = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    per_rank = count // len(ranks)
    prev_rank_ids = [None]
    for rank in ranks:
        current_rank_ids = []
        for _ in range(per_rank):
            taxon_id = str(uuid4())
            parent_id = random.choice(prev_rank_ids)
            taxons.append({
                'id': taxon_id,
                'parent_id': parent_id,
                'name': fake.unique.word().capitalize(),
                'rank': rank
            })
            current_rank_ids.append(taxon_id)
        prev_rank_ids = current_rank_ids
    return taxons

def generate_animals(count, species_ids):
    return [
        {
            'id': str(uuid4()),
            'taxon_id': random.choice(species_ids),
            'name': fake.first_name(),
            'species': fake.word().capitalize(),
            'habitat': fake.word(),
            'created_at': fake.date_time_this_year().isoformat(),
            'updated_at': fake.date_time_this_year().isoformat()
        }
        for _ in range(count)
    ]

def generate_followers(count, user_ids):
    followers_data = []
    unique_pairs = set()
    num_users = len(user_ids)
    max_possible = num_users * (num_users - 1)
    target_count = min(count, max_possible)
    avg_per_user = target_count // num_users if num_users > 0 else 0
    for u1 in user_ids:
        if len(unique_pairs) >= target_count:
            break
        n = random.randint(0, avg_per_user * 2)
        others = [u for u in user_ids if u != u1]
        to_follow = random.sample(others, min(n, len(others), target_count - len(unique_pairs)))
        for u2 in to_follow:
            unique_pairs.add((u1, u2))
    for f_id, f_ed_id in unique_pairs:
        followers_data.append({
            'follower_id': f_id,
            'followed_id': f_ed_id,
            'created_at': fake.date_time_this_year().isoformat()
        })
    return followers_data

def generate_post_like(count, user_ids, post_ids):
    post_like_data = []
    unique_pairs = set()
    max_possible = len(user_ids) * len(post_ids)
    target_count = min(count, max_possible)
    while len(unique_pairs) < target_count:
        u_id = random.choice(user_ids)
        p_id = random.choice(post_ids)
        unique_pairs.add((u_id, p_id))
    for u_id, p_id in unique_pairs:
        post_like_data.append({
            'user_id': u_id,
            'post_id': p_id,
            'created_at': fake.date_time_this_year().isoformat()
        })
    return post_like_data

def generate_comment_like(count, user_ids, comment_ids):
    comment_like_data = []
    unique_pairs = set()
    max_possible = len(user_ids) * len(comment_ids)
    target_count = min(count, max_possible)
    while len(unique_pairs) < target_count:
        u_id = random.choice(user_ids)
        c_id = random.choice(comment_ids)
        unique_pairs.add((u_id, c_id))
    for u_id, c_id in unique_pairs:
        comment_like_data.append({
            'user_id': u_id,
            'comment_id': c_id,
            'created_at': fake.date_time_this_year().isoformat()
        })
    return comment_like_data

def generate_post_tag(max_per_post, posts, tags):
    post_tag_data = []
    tag_ids = [t['id'] for t in tags]
    for post in posts:
        n = random.randint(1, max_per_post)
        selected_tags = random.sample(tag_ids, min(n, len(tag_ids)))
        for tag_id in selected_tags:
            post_tag_data.append({
                'post_id': post['id'],
                'tag_id': tag_id,
                'created_at': fake.date_time_this_year().isoformat()
            })
    return post_tag_data

def generate_all(counts):
    users = generate_users(counts['user'])
    user_ids = [u['id'] for u in users]
    taxons = generate_taxons(counts['taxon'])
    species_ids = [t['id'] for t in taxons if t['rank'] == 'Species']
    tags = generate_tags(counts['tag'])
    animals = generate_animals(counts['animal'], species_ids)
    animal_ids = [a['id'] for a in animals]
    posts = generate_posts(counts['post'], user_ids, animal_ids)
    post_ids = [p['id'] for p in posts]
    comments = generate_comments(counts['comment'], user_ids, post_ids, 0.2)
    comment_ids = [c['id'] for c in comments]
    return {
        "user": users,
        "taxon": taxons,
        "tag": tags,
        "animal": animals,
        "post": posts,
        "comment": comments,
        "post_tag": generate_post_tag(counts['post_tag_max'], posts, tags),
        "post_like": generate_post_like(counts['post_like'], user_ids, post_ids),
        "comment_like": generate_comment_like(counts['comment_like'], user_ids, comment_ids),
        "follower": generate_followers(counts['follower'], user_ids)
    }