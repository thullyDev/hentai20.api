from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.handlers.response_handler import ResponseHandler
from app.resources.errors import CRASH
from typing import Any, Dict, Optional, Union
from app.routers.hentai20.hentai20 import (
     get_panels,
     get_manga,
     download_image_from_url,
     get_filter_mangas
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

# https://hentai20.io/manga/?genre%5B%5D=1655&status=ongoing&type=manhwa&order=update
# https://hentai20.io/manga/?genre[]=1655&status=ongoing&type=manhwa&order=update
# TODO: add the filtering 
@router.get("/filter")
async def filter_mangas(
     page: str = "1", 
     genre: Optional[str] = None, 
     status: Optional[str] = None, 
     _type: Optional[str] = None, 
     sort: Optional[str] = None, 
     ) -> JSONResponse:
     params = {
          "page": page
     }
     
     if status:
          params["status"] = status

     if _type:
          params["type"] = _type

     if sort:
          params["order"] = sort

     if genre:
          params["genre[]"] = genre


     data: Union[Dict[str, Any], int] = await get_filter_mangas(endpoint=f"/manga/", params=params)
     
     if data == CRASH or type(data) is int:
          return response.bad_request_response()

     return response.successful_response({ "data": data })


@router.get("/{manga_id}")
async def manga(manga_id: str) -> JSONResponse:
     data: Union[Dict[str, Any], int] = await get_manga(manga_id=manga_id)

     if data == CRASH:
          return response.bad_request_response()

     return response.successful_response({"data": data })

@router.get("/read/{chapter_id}")
async def read(chapter_id: str) -> JSONResponse:
     data: Union[Dict[str, Any], int] = await get_panels(chapter_id=chapter_id)

     if data == CRASH:
          return response.bad_request_response()

     return response.successful_response({"data": data })


