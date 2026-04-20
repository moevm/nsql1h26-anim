from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from enum import Enum

class BaseSchema(BaseModel):
  model_config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True,
    from_attributes=True 
  )

class PostType(str, Enum):
  note = "note"
  animal = "animal"

class TaxonRank(str, Enum):
  kingdom = "kingdom"   
  phylum = "phylum"     
  class_rank = "class"  
  order = "order"       
  family = "family"     
  genus = "genus"      
  species = "species"

  def parent_rank(self) -> "TaxonRank | None":
    ranks = list(TaxonRank)
    idx = ranks.index(self)
    return ranks[idx - 1] if idx > 0 else None