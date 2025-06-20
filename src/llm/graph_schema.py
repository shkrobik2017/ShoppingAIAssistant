from typing import TypedDict, List, Optional, Dict, Any

from src.llm.agents.product_finder.schemas import ProductInfo


class AgentState(TypedDict, total=False):
    user_input: str
    budget: float
    plan: Optional[str]
    user_intent: Optional[str]
    servings: Optional[str]
    recipes: Optional[List[str]]
    products: Optional[List[ProductInfo]]
    total_cost: Optional[float]
    within_budget: Optional[bool]
    retry_attempts: Optional[int]
    final_budget_status: Optional[str]
    final_message: Optional[str]
    __next__: Optional[str]