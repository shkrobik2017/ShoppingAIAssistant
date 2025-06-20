from typing import Union

from openai import OpenAI
from fastapi.responses import JSONResponse

from settings import settings
from src.llm.graph import graph
from src.llm.graph_schema import AgentState
from src.logger.logger import logger

client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def transcribe_audio(file_path: str) -> Union[str, JSONResponse]:
    """
    Transcribe audio file using OpenAI Whisper model.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        Union[str, JSONResponse]: Transcribed text if successful, otherwise JSON error response.
    """
    try:
        with open(file_path, "rb") as audio_f:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_f
            )
        return transcript_response.text
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return JSONResponse(
            {
                "message": "File saved, but transcription failed",
                "error": str(e)
            },
            status_code=500
        )


async def run_graph(request_content: str) -> Union[str, JSONResponse]:
    """
    Execute the LangGraph multi-agent workflow based on transcribed input.

    Args:
        request_content (str): The transcribed user input.

    Returns:
        Union[str, JSONResponse]: Final message from the graph or JSON error response if failed.
    """
    try:
        initial_state: AgentState = {
            "user_input": request_content,
            "budget": 9999  # Default large budget; adjust as needed
        }
        graph_result = await graph.ainvoke(initial_state)

        final_message = graph_result.get("final_message", "No final message generated.")
        return final_message
    except Exception as e:
        logger.error(f"Graph processing failed: {e}")
        return JSONResponse(
            {
                "message": "Transcription succeeded, but graph processing failed",
                "error": str(e)
            },
            status_code=500
        )
