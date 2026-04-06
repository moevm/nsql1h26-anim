

def seed_users_neo(raw_users: list) -> tuple[list, str]:
    users = [
        {
            'id':         u['id'],
            'email':      u['email'],
            'username':   u['username'],
            'password':   u['password'],
            'role':       u['role'],
            'first_name': u['first_name'],
            'last_name':  u['last_name'],
            'bio':        u['bio'],
            'avatar_url': u['avatar_url'],
            'location':   u['location'],
            'created_at': u['created_at'],
        }
        for u in raw_users
    ]

    query = """
    UNWIND $users AS u
    CREATE (n:User)
    SET n = u
    """

    return users, query

def seed_taxons_neo(raw_taxons: list) -> tuple[list, str]:
    taxons = [
        {
            'id':        t['id'],
            'name':      t['name'],
            'rank':      t['rank'],
        }
        for t in raw_taxons
    ]

    query = """
    UNWIND $taxons AS t
    CREATE (n:Taxon)
    SET n = t
    """

    return taxons, query

def seed_taxon_hierarchy_neo(raw_taxons: list) -> tuple[list, str]:
    """PARENT_OF edges между таксонами по parent_id."""

    edges = [
        {'parent_id': t['parent_id'], 'child_id': t['id']}
        for t in raw_taxons
        if t['parent_id'] is not None
    ]

    query = """
    UNWIND $edges AS e
    MATCH (parent:Taxon {id: e.parent_id})
    MATCH (child:Taxon  {id: e.child_id})
    CREATE (parent)-[:PARENT_OF]->(child)
    """

    return edges, query

def seed_posts_neo(raw_posts: list) -> tuple[list, str]:
    posts = [
        {
            'id':         p['id'],
            'title':      p['title'],
            'content':    p['content'],
            'image_url':  p['image_url'],
            'location':   p['location'],
            'created_at': p['created_at'],
            'updated_at': p['updated_at'],
        }
        for p in raw_posts
    ]

    query = """
    UNWIND $posts AS p
    CREATE (n:Post)
    SET n = p
    """

    return posts, query

def seed_comments_neo(raw_comments: list) -> tuple[list, str]:
    comments = [
        {
            'id':         c['id'],
            'content':    c['content'],
            'created_at': c['created_at'],
            'updated_at': c['updated_at'],
        }
        for c in raw_comments
    ]

    query = """
    UNWIND $comments AS c
    CREATE (n:Comment)
    SET n = c
    """

    return comments, query


def seed_tags_neo(raw_tags: list) -> tuple[list, str]:
    tags = [
        {
            'id':   t['id'],
            'name': t['name'],
        }
        for t in raw_tags
    ]

    query = """
    UNWIND $tags AS t
    MERGE (n:Tag {name: t.name})
    ON CREATE SET n = t
    """

    return tags, query

def seed_animals_neo(raw_animals: list) -> tuple[list, str]:
    animals = [
        {
            'id':         a['id'],
            'name':       a['name'],
            'species':    a['species'],
            'habitat':    a['habitat'],
            'created_at': a['created_at'],
            'updated_at': a['updated_at'],
        }
        for a in raw_animals
    ]

    query = """
    UNWIND $animals AS a
    CREATE (n:Animal)
    SET n = a
    """

    return animals, query

def seed_animal_belonged_to_taxon_neo(raw_animals: list) -> tuple[list, str]:
    """Animal -[:BELONGED_TO]-> Taxon"""
    
    edges = [
        {'animal_id': a['id'], 'taxon_id': a['taxon_id']}
        for a in raw_animals
    ]
    query = """
    UNWIND $edges AS e
    MATCH (a:Animal {id: e.animal_id})
    MATCH (t:Taxon  {id: e.taxon_id})
    CREATE (a)-[:BELONGED_TO]->(t)
    """

    return edges, query

def seed_user_authored_post_neo(raw_posts: list) -> tuple[list, str]:
    """User -[:AUTHORED]-> Post"""
    
    edges = [
        {'user_id': p['user_id'], 'post_id': p['id']}
        for p in raw_posts
    ]

    query = """
    UNWIND $edges AS e
    MATCH (u:User {id: e.user_id})
    MATCH (p:Post {id: e.post_id})
    CREATE (u)-[:AUTHORED]->(p)
    """

    return edges, query

def seed_post_observed_animal_neo(raw_posts: list) -> tuple[list, str]:
    """Post -[:OBSERVED]-> Animal"""

    edges = [
        {'post_id': p['id'], 'animal_id': p['animal_id']}
        for p in raw_posts
    ]

    query = """
    UNWIND $edges AS e
    MATCH (p:Post   {id: e.post_id})
    MATCH (a:Animal {id: e.animal_id})
    CREATE (p)-[:OBSERVED]->(a)
    """

    return edges, query

def seed_post_tagged_neo(raw_post_tags: list) -> tuple[list, str]:
    """Post -[:TAGGED]-> Tag"""

    query = """
    UNWIND $edges AS e
    MATCH (p:Post {id: e.post_id})
    MATCH (t:Tag  {id: e.tag_id})
    CREATE (p)-[:TAGGED {created_at: e.created_at}]->(t)
    """

    return raw_post_tags, query

def seed_post_likes_neo(raw_post_likes: list) -> tuple[list, str]:
    """User -[:LIKED]-> Post"""

    query = """
    UNWIND $edges AS e
    MATCH (u:User {id: e.user_id})
    MATCH (p:Post {id: e.post_id})
    CREATE (u)-[:LIKED {created_at: e.created_at}]->(p)
    """

    return raw_post_likes, query

def seed_user_authored_comment_neo(raw_comments: list) -> tuple[list, str]:
    """User -[:AUTHORED]-> Comment"""
    
    edges = [
        {'user_id': c['user_id'], 'comment_id': c['id']}
        for c in raw_comments
    ]

    query = """
    UNWIND $edges AS e
    MATCH (u:User    {id: e.user_id})
    MATCH (c:Comment {id: e.comment_id})
    CREATE (u)-[:AUTHORED]->(c)
    """

    return edges, query

def seed_comment_on_post_neo(raw_comments: list) -> tuple[list, str]:
    """Comment -[:ON]-> Post"""
    
    edges = [
        {'comment_id': c['id'], 'post_id': c['post_id']}
        for c in raw_comments
    ]

    query = """
    UNWIND $edges AS e
    MATCH (c:Comment {id: e.comment_id})
    MATCH (p:Post    {id: e.post_id})
    CREATE (c)-[:ON]->(p)
    """

    return edges, query

def seed_comment_replied_neo(raw_comments: list) -> tuple[list, str]:
    """Comment -[:REPLIED]-> Comment """

    edges = [
        {'child_id': c['id'], 'parent_id': c['parent_id']}
        for c in raw_comments
        if c['parent_id'] is not None
    ]

    query = """
    UNWIND $edges AS e
    MATCH (child:Comment  {id: e.child_id})
    MATCH (parent:Comment {id: e.parent_id})
    CREATE (child)-[:REPLIED]->(parent)
    """

    return edges, query
 
 
def seed_comment_liked_neo(raw_comment_likes: list) -> tuple[list, str]:
    """User -[:LIKED]-> Comment"""

    query = """
    UNWIND $edges AS e
    MATCH (u:User    {id: e.user_id})
    MATCH (c:Comment {id: e.comment_id})
    CREATE (u)-[:LIKED {created_at: e.created_at}]->(c)
    """

    return raw_comment_likes, query
 
 
def seed_follows_neo(raw_followers: list) -> tuple[list, str]:
    """User -[:FOLLOWED]-> User"""

    edges = [
        {
            'follower_id': f['follower_id'],
            'followed_id': f['followed_id'],
            'created_at':  f['created_at'],
        }
        for f in raw_followers
    ]

    query = """
    UNWIND $edges AS e
    MATCH (follower:User {id: e.follower_id})
    MATCH (followed:User {id: e.followed_id})
    CREATE (follower)-[:FOLLOWED {created_at: e.created_at}]->(followed)
    """

    return edges, query

def seed_taxons_sql(raw_taxons):
    query = """
    INSERT INTO taxon (id, parent_id, name, rank)
    VALUES (%(id)s, %(parent_id)s, %(name)s, %(rank)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_taxons, query

def seed_tags_sql(raw_tags):
    query = """
    INSERT INTO tag (id, name)
    VALUES (%(id)s, %(name)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_tags, query

def seed_users_sql(raw_users):
    query = """
    INSERT INTO "user" (id, email, password, username, role, first_name, last_name, bio, avatar_url, created_at)
    VALUES (%(id)s, %(email)s, %(password)s, %(username)s, %(role)s, %(first_name)s, %(last_name)s, %(bio)s, %(avatar_url)s, %(created_at)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_users, query

def seed_animals_sql(raw_animals):
    query = """
    INSERT INTO animal (id, taxon_id, name, species, habitat)
    VALUES (%(id)s, %(taxon_id)s, %(name)s, %(species)s, %(habitat)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_animals, query

def seed_posts_sql(raw_posts):
    query = """
    INSERT INTO post (id, user_id, animal_id, location, title, content, image_url, created_at, updated_at)
    VALUES (%(id)s, %(user_id)s, %(animal_id)s, %(location)s, %(title)s, %(content)s, %(image_url)s, %(created_at)s, %(updated_at)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_posts, query

def seed_comments_sql(raw_comments):
    query = """
    INSERT INTO comment (id, user_id, post_id, parent_id, content, created_at, updated_at)
    VALUES (%(id)s, %(user_id)s, %(post_id)s, %(parent_id)s, %(content)s, %(created_at)s, %(updated_at)s)
    ON CONFLICT (id) DO NOTHING
    """

    return raw_comments, query

def seed_post_tags_sql(raw_post_tags):
    query = """
    INSERT INTO post_tag (post_id, tag_id)
    VALUES (%(post_id)s, %(tag_id)s)
    ON CONFLICT DO NOTHING
    """

    return raw_post_tags, query

def seed_post_likes_sql(raw_post_likes):
    query = """
    INSERT INTO post_like (user_id, post_id, created_at)
    VALUES (%(user_id)s, %(post_id)s, %(created_at)s)
    ON CONFLICT DO NOTHING
    """

    return raw_post_likes, query

def seed_comment_likes_sql(raw_comment_likes):
    query = """
    INSERT INTO comment_like (user_id, comment_id, created_at)
    VALUES (%(user_id)s, %(comment_id)s, %(created_at)s)
    ON CONFLICT DO NOTHING
    """

    return raw_comment_likes, query

def seed_followers_sql(raw_followers):
    query = """
    INSERT INTO follower (follower_id, followed_id, created_at)
    VALUES (%(follower_id)s, %(followed_id)s, %(created_at)s)
    ON CONFLICT DO NOTHING
    """

    return raw_followers, query