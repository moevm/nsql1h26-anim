from repositories.base import BaseRepository
from models.tag import Tag
from core.constants import NodeLabels as N, RelationTypes as R

class TagRepository(BaseRepository[Tag]):
    def __init__(self, db):
        super().__init__(db, N.TAG, Tag)