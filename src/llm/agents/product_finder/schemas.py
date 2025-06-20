from typing import List
from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    name: str = Field(..., description="The store product name.")
    price: float = Field(..., description="The price of the product.")
    manufacturer: str = Field(..., description="The manufacturer of the product.")
    composition: str = Field(..., description="The main composition or key ingredients of the product.")

class ProductFinderStructuredSchema(BaseModel):
    products: List[ProductInfo] = Field(
        ...,
        description=(
            "A list of product dictionaries selected for the user's ingredients. "
            "Each product dictionary contains 'name', 'price', 'manufacturer', and 'composition'. "
            "Example: ["
            "{\"name\": \"Fresh Mozzarella 250g\", \"price\": 4.0, "
            "\"manufacturer\": \"CheeseCo\", \"composition\": \"milk, salt, enzymes\"}, "
            "{\"name\": \"Fresh Tomatoes 500g\", \"price\": 3.0, "
            "\"manufacturer\": \"FarmFresh\", \"composition\": \"tomatoes\"}]"
        )
    )


