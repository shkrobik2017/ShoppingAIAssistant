from typing import Optional

from pydantic import BaseModel, Field

from src.db.product.enums import ProductCategoryEnum


class Product(BaseModel):
    name: str = Field(..., description="Name of the product.")
    price: float = Field(..., description="Product's price.")
    category: ProductCategoryEnum = Field(..., description="Product's category.")
    manufacturer: str = Field(..., description="Product's manufacturer.")
    composition: str = Field(..., description="Product's composition.")

class UpdateProduct(BaseModel):
    name: Optional[str] = Field(None, description="Name of the product.")
    price: Optional[float] = Field(None, description="Product's price.")
    category: Optional[ProductCategoryEnum] = Field(None, description="Product's category.")
    manufacturer: Optional[str] = Field(None, description="Product's manufacturer.")
    composition: Optional[str] = Field(None, description="Product's composition.")