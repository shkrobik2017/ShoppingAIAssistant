from fastapi import APIRouter
from typing import Dict

from src.routers.products.schemas import Product, UpdateProduct
from src.routers.products.services import (
    get_product_from_db,
    create_product_in_db,
    update_product_in_db,
    delete_product_in_db
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get(
    path="/{name}",
    response_model=Product,
    summary="Retrieve a product by name",
    description="Fetch a product from the database using its name."
)
async def get_product(name: str) -> Product:
    """
    Get a product by its name.

    Args:
        name (str): The request containing the product name.

    Returns:
        Product: The product data retrieved from the database.
    """
    return await get_product_from_db(name=name)


@router.post(
    path="/",
    response_model=Product,
    summary="Create a new product",
    description="Create and store a new product in the database."
)
async def create_product(create_request: Product) -> Product:
    """
    Create a new product.

    Args:
        create_request (Product): The product data to create.

    Returns:
        Product: The created product data.
    """
    return await create_product_in_db(product_data=create_request)


@router.put(
    path="/{name}",
    response_model=Product,
    summary="Update an existing product",
    description="Update the details of an existing product by its name."
)
async def update_product(name: str, update_request: UpdateProduct) -> Product:
    """
    Update an existing product by name.

    Args:
        name (str): The name of the product to update.
        update_request (UpdateProduct): The updated product data.

    Returns:
        Product: The updated product data.
    """
    return await update_product_in_db(name=name, product_data=update_request)


@router.delete(
    path="/{name}",
    summary="Delete a product",
    description="Delete a product from the database by its name."
)
async def delete_product(name: str) -> Dict[str, bool]:
    """
    Delete a product by name.

    Args:
        name (str): The name of the product to delete.

    Returns:
        Dict[str, bool]: The status of the deletion operation.
    """
    status = await delete_product_in_db(name=name)
    return {"success": status}
