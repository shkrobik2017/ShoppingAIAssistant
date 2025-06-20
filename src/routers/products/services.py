from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist

from src.db.product.model import ProductModel
from src.db.product.repository import (
    get_product_by_name,
    create_product,
    update_product,
    delete_product
)
from src.routers.products.schemas import Product, UpdateProduct


def product_to_pydantic(product: ProductModel) -> Product:
    return Product(
        name=product.name,
        price=product.price,
        category=product.category,
        manufacturer=product.manufacturer,
        composition=product.composition
    )


async def get_product_from_db(*, name: str) -> Product:
    """
    Get a product by its name.

    Args:
        name: The product name.

    Returns:
        Product: The product data.

    Raises:
        HTTPException: If the product does not exist.
    """
    product = await get_product_by_name(name=name)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product_to_pydantic(product)


async def create_product_in_db(*, product_data: Product) -> Product:
    """
    Create a new product in the database.

    Args:
        product_data: Product data to create.

    Returns:
        Product: The created product.
    """
    product = await create_product(**product_data.model_dump())
    return product_to_pydantic(product)


async def update_product_in_db(*, name: str, product_data: UpdateProduct) -> Product:
    """
    Update an existing product.

    Args:
        name: The name of the product to update.
        product_data: The fields to update.

    Returns:
        Product: The updated product.

    Raises:
        HTTPException: If the product does not exist.
    """
    try:
        product = await get_product_by_name(name=name)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    await update_product(product=product, update_data=update_data)

    return product_to_pydantic(product)


async def delete_product_in_db(name: str) -> bool:
    """
    Delete a product by its name.

    Args:
        name: The product name.

    Returns:
        bool: Whether deletion was successful.
    """
    try:
        deleted = await delete_product(name=name)
        return deleted > 0
    except Exception:
        return False

