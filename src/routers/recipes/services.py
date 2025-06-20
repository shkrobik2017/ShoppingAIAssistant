from fastapi import HTTPException, status
from src.db.recipe.repository import (
    get_recipe_by_name,
    create_recipe,
    update_recipe,
    delete_recipe
)
from src.routers.recipes.schemas import Recipe, UpdateRecipe
from src.db.recipe.model import RecipeModel


def recipe_to_pydantic(recipe: RecipeModel) -> Recipe:
    """
    Convert a RecipeModel instance to a Recipe Pydantic model.

    Args:
        recipe (RecipeModel): ORM recipe instance.

    Returns:
        Recipe: The Pydantic representation of the recipe.
    """
    return Recipe(
        name=recipe.name,
        category=recipe.category,
        ingredients=recipe.ingredients
    )


async def _get_existing_recipe(name: str) -> RecipeModel:
    """
    Internal helper to retrieve an existing recipe or raise 404.

    Args:
        name (str): Name of the recipe.

    Returns:
        RecipeModel: The ORM recipe instance.

    Raises:
        HTTPException: If the recipe is not found.
    """
    recipe = await get_recipe_by_name(name=name)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return recipe


async def get_recipe_from_db(*, name: str) -> Recipe:
    """
    Retrieve a recipe by name.

    Args:
        name (str): Recipe name.

    Returns:
        Recipe: The recipe data.
    """
    recipe = await _get_existing_recipe(name)
    return recipe_to_pydantic(recipe)


async def create_recipe_in_db(*, recipe_data: Recipe) -> Recipe:
    """
    Create a new recipe if it doesn't exist.

    Args:
        recipe_data (Recipe): Data for the new recipe.

    Returns:
        Recipe: The created recipe data.
    """
    recipe = await create_recipe(
        name=recipe_data.name,
        category=recipe_data.category,
        ingredients=[ingredient.model_dump() for ingredient in recipe_data.ingredients]
    )
    return recipe_to_pydantic(recipe)


async def update_recipe_in_db(*, name: str, recipe_data: UpdateRecipe) -> Recipe:
    """
    Update a recipe's fields.

    Args:
        name (str): Recipe name.
        recipe_data (UpdateRecipe): Data to update.

    Returns:
        Recipe: The updated recipe data.
    """
    recipe = await _get_existing_recipe(name)
    update_data = recipe_data.model_dump(exclude_unset=True)
    await update_recipe(recipe=recipe, update_data=update_data)
    return recipe_to_pydantic(recipe)


async def delete_recipe_in_db(name: str) -> bool:
    """
    Delete a recipe by name.

    Args:
        name (str): Recipe name.

    Returns:
        bool: True if deleted, False otherwise.
    """
    try:
        deleted = await delete_recipe(name=name)
        return deleted > 0
    except Exception:
        return False
