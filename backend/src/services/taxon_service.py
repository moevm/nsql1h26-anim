from schemas.base import TaxonRank
from schemas.request import TaxonCreate
from database.db import db
from database.models import Taxon
from core.utils import generate_uid

async def merge_taxon(taxon: TaxonCreate) -> Taxon:
    parent_rank = taxon.rank.parent_rank()
    taxon_id = generate_uid()
    parent_taxon_id = generate_uid()

    if taxon.rank == TaxonRank.kingdom and taxon.parent_name:
        raise ValueError("Kingdom rank cannot have a parent taxon.")

    query = """
    MERGE (tx:Taxon {name: $name, rank: $rank})
    ON CREATE SET tx.id = $tx_id
    
    WITH tx
    FOREACH (_ IN CASE WHEN $parent_name IS NOT NULL AND $parent_rank IS NOT NULL THEN [1] ELSE [] END |
        MERGE (parent:Taxon {name: $parent_name, rank: $parent_rank})
        ON CREATE SET parent.id = $parent_id
        MERGE (parent)-[:PARENT_OF]->(tx)
    )
    
    RETURN tx.id AS id, tx.name AS name, tx.rank AS rank
    """
    
    result = await db.query(
        query, 
        name=taxon.name, 
        rank=taxon.rank,
        tx_id=taxon_id,
        parent_id=parent_taxon_id,
        parent_name=taxon.parent_name,
        parent_rank=parent_rank
    )

    if not result:
        raise RuntimeError(f"Could not create/merge taxon: {taxon.name}")
    
    return Taxon(
        id=result[0]['id'],
        name=result[0]['name'],
        rank=result[0]['rank']
    )

async def get_chain(taxon_id: str) -> list[Taxon]:
  query = """
  MATCH (tx:Taxon {id: $taxon_id})
  OPTIONAL MATCH chain = (tx)<-[:PARENT_OF*0..6]-(ancestor:Taxon)
  RETURN [node IN nodes(chain) | {name: node.name, rank: node.rank, id: node.id}] AS chain
  """
  
  result = await db.query(query, taxon_id=taxon_id)
  if not result or not result[0]['chain']:
    return []
  
  return [Taxon(**t) for t in result[0]["chain"]]