from tortoise.contrib.pydantic import pydantic_model_creator

from src.db.product.model import ProductModel
from src.db.recipe.model import RecipeModel

ProductPydantic = pydantic_model_creator(ProductModel)
RecipePydantic = pydantic_model_creator(RecipeModel)