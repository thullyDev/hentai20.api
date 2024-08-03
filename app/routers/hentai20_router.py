from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.handlers.response_handler import ResponseHandler
from app.resources.errors import CRASH
from typing import Any, Dict, Optional, Union
from app.routers.hentai20.hentai20 import (
     get_panels,
     download_image_from_url,
)
from fastapi.responses import FileResponse, StreamingResponse

router: APIRouter = APIRouter(prefix="/hentai")
response: ResponseHandler = ResponseHandler()

@router.get("/proxy/{image_url:path}")
def proxy(image_url: Optional[str] = None):
     image_bytes = download_image_from_url(image_url)

     if not image_bytes:
          return FileResponse("media/error.gif", media_type="image/gif")

     return StreamingResponse(iter([image_bytes]), media_type="image/jpeg")

@router.get("/{chapter_id}")
async def read(chapter_id: str) -> JSONResponse:
     data: Union[Dict[str, Any], int] = await get_panels(chapter_id=chapter_id)

     if data == CRASH:
          return response.bad_request_response()

     return response.successful_response({"data": data })


