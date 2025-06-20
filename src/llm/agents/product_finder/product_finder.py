from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage

from src.db.product.repository import get_product_by_category
from src.db.recipe.repository import get_recipe_by_name
from src.llm.agents.common.base_agent import BaseLLMAgent
from src.llm.agents.product_finder.schemas import ProductFinderStructuredSchema, ProductInfo
from src.llm.graph_schema import AgentState
from src.logger.logger import logger
from src.redis_client.client import cache
from src.redis_client.services import make_cache_key


class ProductFinderAgent(BaseLLMAgent):
    """
    ProductFinderAgent is responsible for selecting suitable store products
    for the ingredients of the selected recipes using an LLM.
    """

    def __init__(self) -> None:
        """
        Initialize the ProductFinderAgent with the appropriate LLM client.
        """
        super().__init__()

    @staticmethod
    async def get_recipe(name: str) -> Any:
        """
        Retrieve a recipe by its name.

        Args:
            name (str): The name of the recipe.

        Returns:
            Any: The recipe object or None if not found.
        """
        return await get_recipe_by_name(name=name)

    async def create_prompt(self, recipes: List[str]) -> str:
        """
        Construct a prompt for the LLM using the recipes and their associated products.

        Args:
            recipes (List[str]): A list of recipe names.

        Returns:
            str: The assembled prompt text for the LLM.
        """
        prompt_text = await self.get_prompt(agent_name=Path(__file__).parent.name)
        products: Dict[str, List[Any]] = defaultdict(list)

        for name in recipes:
            recipe = await self.get_recipe(name=name)
            if not recipe or not recipe.ingredients:
                logger.warning(f"Recipe '{name}' not found or has no ingredients.")
                continue

            for ingredient in recipe.ingredients:
                category = ingredient.get("category")
                if not category:
                    logger.warning(f"Ingredient in '{name}' missing category: {ingredient}")
                    continue

                product = await get_product_by_category(category=category)
                if product:
                    products[name].append(product)
                else:
                    logger.warning(f"No product found for category '{category}' in recipe '{name}'.")

        messages = [
            SystemMessage(content=prompt_text),
            HumanMessage(content=f"Recipes for user: {recipes}"),
            SystemMessage(content=f"Products for recipes ingredients: {products}")
        ]

        final_request = "\n".join([message.content for message in messages])
        logger.info(f"ProductFinderAgent prompt: {final_request}")
        return final_request

    async def generate(self, user_input: AgentState) -> AgentState:
        """
        Generate the product list for the given recipes using the LLM
        and update the agent state.

        Args:
            user_input (AgentState): The current agent state containing the recipes.

        Returns:
            AgentState: The updated agent state with selected products.
        """
        recipes = user_input.get("recipes", [])
        cache_key = make_cache_key("product_finder", recipes)

        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"ProductFinderAgent cache hit: {cache_key}")
            user_input["products"] = [ProductInfo(**item) for item in cached]
            return user_input

        prompt = await self.create_prompt(recipes)
        llm_with_structured_output = self.llm.with_structured_output(ProductFinderStructuredSchema)
        llm_response = await llm_with_structured_output.ainvoke(prompt)

        logger.info(f"ProductFinderAgent response: {llm_response}")

        products = llm_response.products
        await cache.set(cache_key, [p.model_dump() for p in products])

        user_input["products"] = products
        return user_input
