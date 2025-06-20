from typing import Dict, Any, List, Optional

from src.db.product.enums import ProductCategoryEnum
from src.db.product.model import ProductModel


async def get_product_by_category(*, category: str) -> List[tuple]:
    """
    Retrieve products by category.

    Args:
        category: The category name.

    Returns:
        A list of tuples containing product details.
    """
    return await ProductModel.filter(category=category).values_list(
        "name", "price", "manufacturer", "composition"
    )


async def get_product_by_name(*, name: str) -> Optional[ProductModel]:
    """
    Retrieve a product by its name.

    Args:
        name: The product name.

    Returns:
        The product model instance or None if not found.
    """
    return await ProductModel.get_or_none(name=name)


async def create_product(
    *,
    name: str,
    price: float,
    category: ProductCategoryEnum,
    manufacturer: Optional[str],
    composition: Optional[str]
) -> ProductModel:
    """
    Create a new product if it doesn't already exist.

    Args:
        name: Product name.
        price: Product price.
        category: Product category enum.
        manufacturer: Product manufacturer.
        composition: Product composition.

    Returns:
        The created or existing product model instance.
    """
    product = await get_product_by_name(name=name)
    if not product:
        product = await ProductModel.create(
            name=name,
            price=price,
            category=category,
            manufacturer=manufacturer,
            composition=composition
        )
    return product


async def update_product(
    product: ProductModel,
    update_data: Dict[str, Any]
) -> ProductModel:
    """
    Update product fields with provided data.

    Args:
        product: The product model instance to update.
        update_data: A dictionary of fields and new values.

    Returns:
        The updated product model instance.
    """
    for field, value in update_data.items():
        if getattr(product, field) != value:
            setattr(product, field, value)

    await product.save()
    return product


async def delete_product(name: str) -> int:
    """
    Delete a product by its name.

    Args:
        name: The product name.

    Returns:
        The number of deleted rows.
    """
    return await ProductModel.filter(name=name).delete()
