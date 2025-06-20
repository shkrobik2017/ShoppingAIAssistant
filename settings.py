from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class for application settings, loaded from environment variables.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        frozen = True

    POSTGRES_HOST: str = Field(
        ...,
        description="The hostname of the PostgreSQL database."
    )

    POSTGRES_PORT: int = Field(
        ...,
        description="The port number for connecting to the PostgreSQL database."
    )

    POSTGRES_USER: str = Field(
        ...,
        description="The username for authenticating to the PostgreSQL database."
    )

    POSTGRES_PASSWORD: str = Field(
        ...,
        description="The password for authenticating to the PostgreSQL database."
    )

    POSTGRES_DB: str = Field(
        ...,
        description="The name of the PostgreSQL database to connect to."
    )

    LLM_NAME: str = Field(
        ...,
        description="The name of the language model being used (e.g., 'ollama' or 'openai')."
    )

    OPENAI_API_KEY: str = Field(
        ...,
        description="API key for accessing OpenAI services."
    )

    OPENAI_MODEL: str = Field(
        ...,
        description="The model to be used with OpenAI (e.g., 'gpt-3.5')."
    )

    OLLAMA_BASE_URL: str = Field(
        ...,
        description="Base URL for the Ollama service."
    )

    OLLAMA_MODEL: str = Field(
        ...,
        description="The model to be used with Ollama."
    )

    LANGCHAIN_API_KEY: str = Field(
        ...,
        description="LangSmith API key."
    )

    LANGCHAIN_PROJECT: str = Field(
        ...,
        description="LangSmith project name."
    )

    LANGCHAIN_TRACING_V2: str = Field(
        ...,
        description="LangSmith v2 tracing version."
    )

    REDIS_HOST: str = Field(
        ...,
        description="Redis host."
    )

    REDIS_PORT: str = Field(
        ...,
        description="Redis port"
    )

# Instance of the Settings class, which loads the configuration from the environment.
settings: Settings = Settings()
