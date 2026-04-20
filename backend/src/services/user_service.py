from uuid import uuid4
from database.models import User
from schemas.request import RegisterRequest, UserUpdate
from core.utils import generate_uid, get_now_iso, hash_password 
from database.db import db

async def create_user(data: RegisterRequest) -> User:
  password_hash = hash_password(data.password)
  user = User( 
    id=generate_uid(),
    username=data.username,
    email=data.email,
    password=password_hash,
    first_name=data.first_name,
    last_name=data.last_name,
    created_at=get_now_iso(),
    updated_at=get_now_iso()
  )

  query = """
  CREATE (u:User)
  SET u = $props
  RETURN u
  """

  await db.query(query, props=user.model_dump())
  return user

async def get_initials(user: User) -> str:
  return f"{user.first_name[0]}{user.last_name}".upper()

async def get_user_by_id(id: str) -> User | None:
  query = """
  MATCH (u:User {id: $id})
  RETURN u
  """

  result = await db.query(query, id=id)
  if not result:
    return None

  user_data = result[0]['u']
  return User(**user_data)

async def get_user_by_identifier(identifier: str) -> User | None:
  query = """
  MATCH (u:User)
  WHERE u.email = $identifier OR u.username = $identifier
  RETURN u
  LIMIT 1
  """

  result = await db.query(query, identifier=identifier)

  if not result:
    return None

  return User(**result[0]["u"])
  
async def get_all_users() -> list[User]:
  query = """
  MATCH (u:User)
  RETURN u
  """

  result = await db.query(query)
  if not result:
    return []
        
  return [User(**record['u']) for record in result]
  
async def update_user(id: str, data: UserUpdate) -> User | None:
  update_data = data.model_dump(exclude_none=True)
    
  if not update_data:
    return None
  
  query = """
  MATCH (u: User {id: $id})
  SET u += $props,
      u.updated_at = $updated_at
  RETURN u
  """

  result = await db.query(
    query,
    id=id,
    props=update_data,
    updated_at=get_now_iso()
  )

  if not result:
    return None
  
  user_data = result[0]['u']
  return User(**user_data)

async def delete_user(id: str) -> bool:
  query = """
  MATCH (u:User {id: $id})
  WITH u
  DETACH DELETE u
  RETURN count(u) > 0 AS deleted
  """

  result = await db.query(query, id=id)

  if not result:
    return False

  return result[0]["deleted"]