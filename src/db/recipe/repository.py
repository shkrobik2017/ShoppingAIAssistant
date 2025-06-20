from typing import Dict, Any, Optional, List
from src.db.recipe.model import RecipeModel
from src.db.recipe.enums import RecipeCategoryEnum


async def get_recipe_by_name(*, name: str) -> Optional[RecipeModel]:
    """
    Retrieve a recipe by its name.

    Args:
        name (str): The name of the recipe to retrieve.

    Returns:
        Optional[RecipeModel]: The recipe instance if found, otherwise None.
    """
    return await RecipeModel.get_or_none(name=name)


async def get_recipes() -> List[Dict[str, Any]]:
    """
    Retrieve all recipes with their names and categories.

    Returns:
        List[Dict[str, Any]]: A list of recipes with 'name' and 'category' fields.
    """
    return await RecipeModel.all().values("name", "category")


async def create_recipe(
    *,
    name: str,
    category: RecipeCategoryEnum,
    ingredients: List[Dict[str, Any]]
) -> RecipeModel:
    """
    Create a new recipe if it does not already exist.

    Args:
        name (str): The name of the recipe.
        category (RecipeCategoryEnum): The category of the recipe.
        ingredients (dict): The ingredients of the recipe.

    Returns:
        RecipeModel: The created or existing recipe instance.
    """
    recipe = await get_recipe_by_name(name=name)
    if not recipe:
        recipe = await RecipeModel.create(
            name=name,
            category=category,
            ingredients=ingredients
        )
    return recipe


async def update_recipe(
    recipe: RecipeModel,
    update_data: Dict[str, Any]
) -> RecipeModel:
    """
    Update the specified fields of a recipe.

    Args:
        recipe (RecipeModel): The recipe instance to update.
        update_data (Dict[str, Any]): A dictionary of fields and their new values.

    Returns:
        RecipeModel: The updated recipe instance.
    """
    for field, value in update_data.items():
        setattr(recipe, field, value)
    await recipe.save()
    return recipe


async def delete_recipe(name: str) -> int:
    """
    Delete a recipe by its name.

    Args:
        name (str): The name of the recipe to delete.

    Returns:
        int: The number of records deleted (0 if not found).
    """
    return await RecipeModel.filter(name=name).delete()


