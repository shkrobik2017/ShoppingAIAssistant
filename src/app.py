from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise.transactions import in_transaction

from src.db.db_setup import DB
from src.db.product.model import ProductModel
from src.db.product.enums import ProductCategoryEnum
from src.db.recipe.model import RecipeModel
from src.db.recipe.enums import RecipeCategoryEnum
from src.routers.routers import router

test_products = [
    {
        "name": "Milk",
        "price": 40,
        "manufacturer": "SimpleDairy",
        "composition": "Whole milk, vitamin D",
        "category": ProductCategoryEnum.DAIRY,
    },
    {
        "name": "Bread",
        "price": 25,
        "manufacturer": "Bakery #1",
        "composition": "Wheat flour, yeast, salt, water",
        "category": ProductCategoryEnum.BAKERY,
    },
    {
        "name": "Cheese",
        "price": 150,
        "manufacturer": "CheeseHouse",
        "composition": "Milk, starter culture, salt, enzymes",
        "category": ProductCategoryEnum.DAIRY,
    },
    {
        "name": "Tomato",
        "price": 10,
        "manufacturer": "FarmFresh",
        "composition": "Fresh tomatoes",
        "category": ProductCategoryEnum.VEGETABLES,
    },
    {
        "name": "Olive Oil",
        "price": 200,
        "manufacturer": "Mediterranean Gold",
        "composition": "Extra virgin olive oil",
        "category": ProductCategoryEnum.OILS_FATS,
    },
    {
        "name": "Sugar",
        "price": 15,
        "manufacturer": "SweetCo",
        "composition": "Refined sugar crystals",
        "category": ProductCategoryEnum.SWEETS_DESSERTS,
    },
    {
        "name": "Flour",
        "price": 20,
        "manufacturer": "BakersPro",
        "composition": "Wheat flour",
        "category": ProductCategoryEnum.BAKERY,
    },
    {
        "name": "Yeast",
        "price": 8,
        "manufacturer": "Fermento",
        "composition": "Dry yeast",
        "category": ProductCategoryEnum.BAKERY,
    },
    {
        "name": "Salt",
        "price": 5,
        "manufacturer": "SeaSalt Inc.",
        "composition": "Sea salt",
        "category": ProductCategoryEnum.SPICES_CONDIMENTS,
    },
    {
        "name": "Oregano",
        "price": 12,
        "manufacturer": "HerbFarm",
        "composition": "Dried oregano",
        "category": ProductCategoryEnum.SPICES_CONDIMENTS,
    },
    {
        "name": "Tomato Sauce",
        "price": 30,
        "manufacturer": "Saucy",
        "composition": "Tomato puree, salt, herbs",
        "category": ProductCategoryEnum.SAUCES,
    },
]

test_recipes = [
    {
        "name": "Cheese Sandwich",
        "category": RecipeCategoryEnum.ENTREE,
        "ingredients": [
            {"name": "Milk", "category": ProductCategoryEnum.DAIRY, "weight_grams": 200},
            {"name": "Bread", "category": ProductCategoryEnum.BAKERY, "weight_grams": 100},
            {"name": "Cheese", "category": ProductCategoryEnum.DAIRY, "weight_grams": 50},
        ],
    },
    {
        "name": "Cheese Plate",
        "category": RecipeCategoryEnum.APPETIZER,
        "ingredients": [
            {"name": "Cheese", "category": ProductCategoryEnum.DAIRY, "weight_grams": 150},
        ],
    },
    {
        "name": "Tomato Salad",
        "category": RecipeCategoryEnum.APPETIZER,
        "ingredients": [
            {"name": "Tomato", "category": ProductCategoryEnum.VEGETABLES, "weight_grams": 120},
            {"name": "Olive Oil", "category": ProductCategoryEnum.OILS_FATS, "weight_grams": 30},
            {"name": "Sugar", "category": ProductCategoryEnum.SWEETS_DESSERTS, "weight_grams": 5},
        ],
    },
    {
        "name": "Milkshake",
        "category": RecipeCategoryEnum.DRINKS,
        "ingredients": [
            {"name": "Milk", "category": ProductCategoryEnum.DAIRY, "weight_grams": 300},
            {"name": "Sugar", "category": ProductCategoryEnum.SWEETS_DESSERTS, "weight_grams": 20},
        ],
    },
    {
        "name": "German Apple Cake",
        "category": RecipeCategoryEnum.DESSERT,
        "ingredients": [
            {"name": "Sugar", "category": ProductCategoryEnum.SWEETS_DESSERTS, "weight_grams": 100},
            {"name": "Milk", "category": ProductCategoryEnum.DAIRY, "weight_grams": 200},
            {"name": "Bread", "category": ProductCategoryEnum.BAKERY, "weight_grams": 150},
        ],
    },
    {
        "name": "Simple Pizza",
        "category": RecipeCategoryEnum.ENTREE,
        "ingredients": [
            {"name": "Bread", "category": ProductCategoryEnum.BAKERY, "weight_grams": 150},
            {"name": "Tomato", "category": ProductCategoryEnum.VEGETABLES, "weight_grams": 100},
            {"name": "Cheese", "category": ProductCategoryEnum.DAIRY, "weight_grams": 120},
            {"name": "Olive Oil", "category": ProductCategoryEnum.OILS_FATS, "weight_grams": 15},
        ],
    },
]


async def insert_test_data():
    async with in_transaction():
        for prod in test_products:
            await ProductModel.get_or_create(**prod)
        for rec in test_recipes:
            await RecipeModel.get_or_create(
                name=rec["name"],
                category=rec["category"],
                ingredients=rec["ingredients"],
            )


async def delete_test_data():
    async with in_transaction():
        await ProductModel.all().delete()
        await RecipeModel.all().delete()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await DB.init_orm()
    await insert_test_data()
    yield
    await delete_test_data()
    await DB.close_orm()


app = FastAPI(lifespan=lifespan)

app.include_router(router=router)