from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from src.logger.logger import logger
from src.routers.audio.services import transcribe_audio, run_graph

router = APIRouter(prefix="/audio")
templates = Jinja2Templates(directory="src/template")


@router.get("/")
async def get_audio_page(request: Request):
    """
    Render the index page with audio recorder controls.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered HTML template for audio recording.
    """
    return templates.TemplateResponse("audio.html", {"request": request})


@router.post("/upload-audio/")
async def upload_audio(audio_file: UploadFile = File(...)) -> JSONResponse:
    """
    Handle audio file upload, perform transcription, and run multi-agent graph.

    Args:
        audio_file (UploadFile): The uploaded audio file.

    Returns:
        JSONResponse: Response containing the filename, transcription, and graph final message.
    """
    try:
        file_path = f"user_recording_{audio_file.filename}"
        with open(file_path, "wb") as f:
            f.write(await audio_file.read())
        logger.info(f"Audio file saved: {file_path}")

        transcription = await transcribe_audio(file_path=file_path)

        if isinstance(transcription, JSONResponse):
            return transcription

        final_message = await run_graph(request_content=transcription)

        if isinstance(final_message, JSONResponse):
            return final_message

        return JSONResponse({
            "message": "File saved, transcribed, and processed successfully!",
            "filename": audio_file.filename,
            "transcription": transcription,
            "final_message": final_message
        })

    except Exception as ex:
        logger.error(f"Error in audio transcription or processing: {ex}")
        return JSONResponse(
            {
                "message": "An error occurred during audio processing.",
                "error": str(ex)
            },
            status_code=500
        )


