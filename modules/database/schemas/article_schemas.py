"""Article schemas"""
from pydantic import BaseModel, Field


class ArticleResponse(BaseModel):
    """Article response schema"""

    sku: str = Field(None, description="Sku")
    name: str = Field(None, description="The name of the article")
    price: float = Field(None, description="The price of the article")
    quantity: int = Field(None, description="The quantity of the article")
