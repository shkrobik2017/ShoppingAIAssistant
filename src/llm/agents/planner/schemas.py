from pydantic import BaseModel, Field


class PlanStructuredSchema(BaseModel):
    intent: str = Field(
        ...,
        description="A brief, clear description of the user's goal based on their message (e.g., 'create a dinner menu for 4 people')."
    )
    plan: str = Field(
        ...,
        description="A high-level plan for RecipeAgent to follow when selecting recipes. This should include details like meal type (e.g., dinner, lunch), number of dishes, dietary preferences, or any constraints mentioned by the user."
    )
    servings: str = Field(
        ...,
        description="The number of servings or people the meal is for, as specified by the user. If the user does not specify, return '1'."
    )