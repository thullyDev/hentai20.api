import json
from typing import Any, Dict, Union
from fastapi.responses import JSONResponse, Response
from ..resources import (
    FORBIDDEN, 
    CRASH, 
    SUCCESSFUL, 
    NOT_FOUND_MSG, 
    NOT_FOUND, 
    FORBIDDEN_MSG, 
    CRASH_MSG, 
    SUCCESSFUL_MSG,
    BAD_REQUEST_MSG,
    BAD_REQUEST,
)

class ResponseHandler:
    def json_response(self, status_code: int, data: Dict[str, Any]) -> JSONResponse:
        return JSONResponse(content=data, status_code=status_code) 

    def http_response(self, text: str, status_code: int) -> Response:
        return Response(content=text, status_code=status_code)

    def data_processor(self, data: Dict[str, Any], status_code: int, message: str) -> Dict[str, Any]:
        data = data if data else {}
        data["status_code"] = status_code
        if not data.get("message"): 
            data["message"] = message
        return data

    def forbidden_response(self, data: Dict[str, Any] = {}, **kwargs) -> JSONResponse:
        data = self.data_processor(data=data, status_code=FORBIDDEN, message=FORBIDDEN_MSG)
        return self.json_response(data=data, status_code=FORBIDDEN, **kwargs)

    def successful_response(self, data: Dict[str, Any] = {}, **kwargs) -> JSONResponse:
        data = self.data_processor(data=data, status_code=SUCCESSFUL, message=SUCCESSFUL_MSG)
        return self.json_response(data=data, status_code=SUCCESSFUL, **kwargs)

    def not_found_response(self, data: Dict[str, Any] = {}, **kwargs) -> JSONResponse:
        data = self.data_processor(data=data, status_code=NOT_FOUND, message=NOT_FOUND_MSG)
        return self.json_response(data=data, status_code=NOT_FOUND, **kwargs)

    def crash_response(self, data: Dict[str, Any] = {}, **kwargs) -> JSONResponse:
        data = self.data_processor(data=data, status_code=CRASH, message=CRASH_MSG)
        return self.json_response(data=data, status_code=CRASH, **kwargs)

    def bad_request_response(self, data: Dict[str, Any] = {}, **kwargs) -> JSONResponse:
        data = self.data_processor(data=data, status_code=BAD_REQUEST, message=BAD_REQUEST_MSG)
        return self.json_response(data=data, status_code=BAD_REQUEST, **kwargs)
