from typing import List
from pydantic import BaseModel, Field

class RecipeStructuredSchema(BaseModel):
    names: List[str] = Field(
        ...,
        description=(
            "A list of selected recipe names that match the provided plan, servings, and budget. "
            "The list should contain unique names, without duplicates. Return at least one recipe."
        )
    )
