import aiofiles
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from settings import settings


class BaseLLMAgent:
    """
    Base class for LLM agents.
    Automatically selects the LLM provider based on the configuration.
    """

    def __init__(self) -> None:
        """
        Initialize the LLM client based on the configured provider.

        If `LLM_NAME` is 'openai', uses OpenAI Chat model.
        Otherwise, uses Ollama.
        """
        if settings.LLM_NAME == "openai":
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY
            )
        else:
            self.llm = ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL
            )

    @staticmethod
    async def get_prompt(*, agent_name: str) -> str:
        """
        Asynchronously load the agent's prompt text from a file.

        Args:
            agent_name (str): The name of the agent, corresponding to its folder.

        Returns:
            str: The content of the agent's prompt file.
        """
        file_path = f"src/llm/agents/{agent_name}/agent_role.md"
        async with aiofiles.open(file=file_path, mode="r") as file:
            content = await file.read()
        return content
