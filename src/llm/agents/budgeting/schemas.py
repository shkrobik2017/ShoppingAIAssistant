from pydantic import BaseModel, Field


class BudgetingStructuredSchema(BaseModel):
    within_budget: bool = Field(
        ...,
        description="Indicates whether the total cost of selected products fits within the user's budget. True if within budget or equal, False if over budget."
    )