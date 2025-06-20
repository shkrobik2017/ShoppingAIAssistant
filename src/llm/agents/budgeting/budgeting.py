from pathlib import Path
from typing import List, Tuple

from langchain_core.messages import SystemMessage, HumanMessage

from src.llm.agents.budgeting.schemas import BudgetingStructuredSchema
from src.llm.agents.common.base_agent import BaseLLMAgent
from src.llm.agents.product_finder.schemas import ProductInfo
from src.llm.graph_schema import AgentState
from src.logger.logger import logger
from src.redis_client.client import cache
from src.redis_client.services import make_cache_key


class BudgetingAgent(BaseLLMAgent):
    """
    Agent responsible for determining if selected products fit within the user's budget.
    Uses caching to avoid redundant LLM calls for the same product/budget combination.
    """

    async def create_prompt(self, products: List[ProductInfo], budget: float) -> Tuple[str, float]:
        """
        Create the prompt to send to the LLM.

        Args:
            products (List[ProductInfo]): List of products to consider.
            budget (float): The user's budget.

        Returns:
            Tuple[str, float]: The constructed prompt and total price of the products.
        """
        prompt_text = await self.get_prompt(agent_name=Path(__file__).parent.name)
        total_price = sum(product.price for product in products)

        messages = [
            SystemMessage(content=prompt_text),
            HumanMessage(content=f"Products total cost: {total_price}"),
            SystemMessage(content=f"The user's budget: {budget}")
        ]

        final_prompt = "\n".join(m.content for m in messages)
        logger.info(f"BudgetingAgent prompt: {final_prompt}")
        return final_prompt, total_price

    async def generate(self, user_input: AgentState) -> AgentState:
        """
        Main agent logic: checks budget fit, uses cache, and updates the state.

        Args:
            user_input (AgentState): The current user input and context.

        Returns:
            AgentState: Updated state including budget evaluation results.
        """
        products: List[ProductInfo] = user_input["products"]
        budget: float = user_input["budget"]

        cache_key = make_cache_key("budgeting", {
            "products": [p.model_dump() for p in products],
            "budget": budget
        })

        cached_result = await cache.get(cache_key)
        if cached_result:
            logger.info(f"BudgetingAgent cache hit: {cache_key}")
            user_input["within_budget"] = cached_result["within_budget"]
            user_input["total_cost"] = cached_result["total_cost"]
            return user_input

        prompt, total_price = await self.create_prompt(products, budget)

        llm_with_structured_output = self.llm.with_structured_output(BudgetingStructuredSchema)
        llm_response = await llm_with_structured_output.ainvoke(prompt)

        logger.info(f"BudgetingAgent LLM response: {llm_response}")

        await cache.set(cache_key, {
            "within_budget": llm_response.within_budget,
            "total_cost": total_price
        })

        user_input["within_budget"] = llm_response.within_budget
        user_input["total_cost"] = total_price

        return user_input

