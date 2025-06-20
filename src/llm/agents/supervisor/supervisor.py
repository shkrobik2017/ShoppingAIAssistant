from typing import List

from src.llm.graph_schema import AgentState
from src.logger.logger import logger


class SupervisorAgent:
    """
    SupervisorAgent determines the next agent in the multi-agent pipeline
    based on the current state of user_input.
    """

    @staticmethod
    async def generate(user_input: AgentState) -> AgentState:
        """
        Analyze the current agent state and set the next agent to invoke.

        The agent flow follows these steps:
        - Planner → Recipe → ProductFinder → Budgeting → Finalizer
        - If the budget is exceeded, retry ProductFinder up to 3 times.

        Args:
            user_input (AgentState): The current state of the multi-agent pipeline.

        Returns:
            AgentState: The updated state with the `__next__` agent specified.
        """
        if not user_input.get("plan"):
            user_input["__next__"] = "Planner"

        elif not user_input.get("recipes") or not isinstance(user_input.get("recipes"), List):
            user_input["__next__"] = "Recipe"

        elif not user_input.get("products") or not isinstance(user_input.get("products"), List):
            user_input["__next__"] = "ProductFinder"

        elif "within_budget" not in user_input or "total_cost" not in user_input:
            user_input["__next__"] = "Budgeting"

        elif user_input.get("within_budget") is False:
            attempts = user_input.get("retry_attempts", 0)
            if attempts < 2:
                user_input["__next__"] = "ProductFinder"
                user_input["retry_attempts"] = attempts + 1
                logger.info(f"Budget exceeded. Retrying with ProductFinderAgent. Attempt {attempts + 1}")
            else:
                user_input["__next__"] = "Finalizer"
                user_input["final_budget_status"] = "Recipe does not fit into budget after 3 attempts"
                logger.info("Budget exceeded after 3 attempts. Proceeding to Finalizer with last recipe.")
        else:
            user_input["__next__"] = "Finalizer"

        return user_input





