from pathlib import Path

from langchain_core.messages import SystemMessage, HumanMessage

from src.llm.agents.common.base_agent import BaseLLMAgent
from src.llm.agents.planner.schemas import PlanStructuredSchema
from src.llm.graph_schema import AgentState
from src.logger.logger import logger


class PlannerAgent(BaseLLMAgent):
    """
    PlannerAgent is responsible for analyzing user input and generating
    a structured plan, including intent and servings, using an LLM.
    """

    def __init__(self) -> None:
        """
        Initialize the PlannerAgent with the appropriate LLM client.
        """
        super().__init__()

    async def create_prompt(self, user_input_content: str) -> str:
        """
        Construct a prompt for the LLM using the provided user input.

        Args:
            user_input_content (str): The raw user input text.

        Returns:
            str: The assembled prompt text for the LLM.
        """
        prompt = await self.get_prompt(agent_name=Path(__file__).parent.name)

        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"User's input: {user_input_content}")
        ]

        final_request = "\n".join([message.content for message in messages])

        logger.info(f"PlannerAgent prompt: {final_request}")
        return final_request

    async def generate(self, user_input: AgentState) -> AgentState:
        """
        Generate a plan, user intent, and servings information based on user input.

        Args:
            user_input (AgentState): The current agent state including the user's message.

        Returns:
            AgentState: The updated agent state with the generated plan, intent, and servings.
        """
        user_message = user_input.get("user_input", "")
        prompt = await self.create_prompt(user_input_content=user_message)

        llm_with_structured_output = self.llm.with_structured_output(PlanStructuredSchema)
        llm_response = await llm_with_structured_output.ainvoke(prompt)

        logger.info(f"PlannerAgent response: {llm_response}")

        user_input["plan"] = llm_response.plan
        user_input["user_intent"] = llm_response.intent
        user_input["servings"] = llm_response.servings

        return user_input
