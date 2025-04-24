from pydantic import BaseModel, Field
from typing import List

class FinancialEntity(BaseModel):
    name: str = Field(description="The name of financial entity.")

class FinancialEntities(BaseModel):
    entities: List[FinancialEntity] = Field(description="The list of Financial Entities")
