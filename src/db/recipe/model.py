from tortoise import fields
from src.db.common.model import CommonModel
from src.db.recipe.enums import RecipeCategoryEnum


class RecipeModel(CommonModel):
    """
    ORM model representing a recipe.

    Attributes:
        name (str): The unique name of the recipe (max 50 characters).
        category (RecipeCategoryEnum): The category of the recipe (e.g., 'Dessert', 'Main course').
        ingredients (dict): A JSON field containing the list of ingredients and their details.
    """
    name: str = fields.CharField(
        max_length=50,
        unique=True,
        description="The unique name of the recipe (max 50 characters)."
    )

    category: RecipeCategoryEnum = fields.CharEnumField(
        RecipeCategoryEnum,
        max_length=20,
        description="The category of the recipe (e.g., Dessert, Main course)."
    )

    ingredients = fields.JSONField(
        description="A JSON object representing the ingredients of the recipe, including name, quantity, category, etc."
    )
