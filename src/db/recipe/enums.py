from enum import Enum


class RecipeCategoryEnum(str, Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    DESSERT = "dessert"
    DRINKS = "drinks"
