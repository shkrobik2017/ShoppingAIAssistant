from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage

from src.llm.agents.common.base_agent import BaseLLMAgent
from src.llm.graph_schema import AgentState
from src.logger.logger import logger


class FinalizerAgent(BaseLLMAgent):
    """
    Finalizer agent that generates the final message for the user
    based on the processed shopping plan and budget data.
    """

    def __init__(self) -> None:
        """
        Initialize the FinalizerAgent and its LLM client.
        """
        super().__init__()

    async def generate(self, user_input: AgentState) -> AgentState:
        """
        Generate the final user message using LLM based on the collected data.

        Args:
            user_input (AgentState): The current agent state containing budget,
                                     recipes, products, plan, etc.

        Returns:
            AgentState: Updated agent state with the final message.
        """
        prompt = await self.get_prompt(agent_name=Path(__file__).parent.name)

        messages = [
            SystemMessage(content=prompt),
            SystemMessage(content=f"Budget check: {'within budget' if user_input.get('within_budget') else 'over budget'}"),
            SystemMessage(content=f"Total cost: {user_input.get('total_cost')}"),
            SystemMessage(content=f"Recipes selected: {user_input.get('recipes')}"),
            SystemMessage(content=f"Products selected: {user_input.get('products')}"),
            SystemMessage(content=f"Plan for the user: {user_input.get('plan')}"),
            HumanMessage(content="Generate a final message for the user based on this data.")
        ]

        llm_response = await self.llm.ainvoke(messages)

        logger.info(f"FinalizerAgent response: {llm_response}")

        user_input["final_message"] = llm_response.content.strip()

        return user_input
