from fastapi import APIRouter, HTTPException, status
from src.routers.recipes.schemas import Recipe, UpdateRecipe
from src.routers.recipes.services import (
    get_recipe_from_db,
    create_recipe_in_db,
    update_recipe_in_db,
    delete_recipe_in_db
)

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/{name}", response_model=Recipe)
async def get_recipe(name: str):
    """
    Retrieve a recipe by its name.

    Args:
        name (str): The request containing the recipe name.

    Returns:
        Recipe: The recipe data.

    Raises:
        HTTPException: If the recipe is not found.
    """
    return await get_recipe_from_db(name=name)


@router.post("/", response_model=Recipe)
async def create_recipe(create_request: Recipe):
    """
    Create a new recipe in the database.

    Args:
        create_request (Recipe): The recipe data to create.

    Returns:
        Recipe: The newly created recipe.
    """
    return await create_recipe_in_db(recipe_data=create_request)


@router.put("/{name}", response_model=Recipe)
async def update_recipe(name: str, update_request: UpdateRecipe):
    """
    Update an existing recipe by its name.

    Args:
        name (str): The name of the recipe to update.
        update_request (UpdateRecipe): The updated fields for the recipe.

    Returns:
        Recipe: The updated recipe data.

    Raises:
        HTTPException: If the recipe is not found.
    """
    return await update_recipe_in_db(name=name, recipe_data=update_request)


@router.delete("/{name}")
async def delete_recipe(name: str):
    """
    Delete a recipe by its name.

    Args:
        name (str): The name of the recipe to delete.

    Returns:
        dict: A success flag indicating if the deletion was successful.

    Raises:
        HTTPException: If the deletion failed.
    """
    success = await delete_recipe_in_db(name=name)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete recipe")
    return {"success": success}

