from schemas.base import BaseSchema
from models.taxon import Taxon 

class AnimalCreate(BaseSchema):
    name: str
    scientific_name: str
    taxon: Taxon


class AnimalUpdate(BaseSchema):
    name: str | None = None
    scientific_name: str | None = None
    taxon: Taxon | None = None


class AnimalResponse(BaseSchema):
    id: str
    name: str
    scientific_name: str
    taxon: Taxon
