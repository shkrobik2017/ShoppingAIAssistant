from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from src.db.product.enums import ProductCategoryEnum
from src.db.recipe.enums import RecipeCategoryEnum

class Ingredients(BaseModel):
    name: str = Field(..., description="The name of the ingredient.")
    category: ProductCategoryEnum = Field(..., description="Category of the product.")
    weight_grams: float = Field(..., description="Product weight in grams.")

class Recipe(BaseModel):
    name: str = Field(..., description="Name of the recipe.")
    category: RecipeCategoryEnum = Field(..., description="Category of the recipe.")
    ingredients: List[Ingredients] = Field(..., description="Ingredients of the recipe.")


class UpdateRecipe(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the recipe.")
    category: Optional[RecipeCategoryEnum] = Field(None, description="Updated category.")
    ingredients: Optional[List[Ingredients]] = Field(None, description="Updated ingredients.")
