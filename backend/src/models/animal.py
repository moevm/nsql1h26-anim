from models.taxon import Taxon
from models.base import BaseNode

class Animal(BaseNode):
    name: str
    scientific_name: str
    taxon: Taxon