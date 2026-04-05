from neo4j import AsyncSession
from uuid import uuid4
from datetime import datetime, timezone
from .seeder import Seeder

class UserSeeder(Seeder):
  
  count: int = 20
  batch_size: int = 5

  async def run(self, session: AsyncSession) -> None:
    users = [
      {
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
      }
      for _ in range(self.count)
    ]
    
    query = """
      UNWIND $users AS u
      CREATE (n:User {
        id: u.id,
        email: u.email,
        password: u.password,
        username: u.username,
        first_name: u.first_name,
        last_name: u.last_name,
        bio: u.bio,
        avatar_url: u.avatar_url,
        role: u.role,
        created_at: u.created_at
      })
    """
    
    for i in range(0, self.count, self.batch_size):
      batch = users[i:i + self.batch_size]
      await session.run(query, users=batch)
    