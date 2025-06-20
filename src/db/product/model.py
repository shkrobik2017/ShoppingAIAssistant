from tortoise import fields

from src.db.common.model import CommonModel
from src.db.product.enums import ProductCategoryEnum


class ProductModel(CommonModel):
    """
    ORM model representing a store product.

    Attributes:
        name (str): The unique name of the product (max 50 characters).
        price (int): The price of the product in whole currency units (e.g., cents, dollars).
        category (ProductCategoryEnum): The category of the product (e.g., Dairy, Vegetables).
        manufacturer (str, optional): The manufacturer of the product. Can be null if unknown.
        composition (str, optional): The main composition or ingredients of the product. Can be null.
    """
    name: str = fields.CharField(
        max_length=50,
        unique=True,
        description="The unique name of the product (max 50 characters)."
    )

    price: int = fields.IntField(
        description="The price of the product in whole currency units."
    )

    category: ProductCategoryEnum = fields.CharEnumField(
        ProductCategoryEnum,
        max_length=20,
        description="The category of the product (e.g., Dairy, Vegetables)."
    )

    manufacturer: str = fields.CharField(
        max_length=50,
        null=True,
        default=None,
        description="The name of the product's manufacturer (optional)."
    )

    composition: str = fields.TextField(
        null=True,
        default=None,
        description="The main composition or ingredients of the product (optional)."
    )

