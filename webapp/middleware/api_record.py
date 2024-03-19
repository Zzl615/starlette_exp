import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request, Message
from starlette.responses import Response
from uvicorn.protocols.utils import get_path_with_query_string, get_client_addr


logger = logging.getLogger(__name__)

class ApiRecordMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, request_max_size: int = 1024, response_max_size: int = 1024):
        super().__init__(app)
        # 默认值设置为1KB，可以根据需要调整
        self._request_max_size = request_max_size
        self._response_max_size = response_max_size
    
    async def _set_record_request_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {"type": "http.request", "body": body}
        request._receive = receive
    
    async def _record_request_body(self, access_log: str, request: Request) -> bytes:
        if "content-length" in request.headers:
            content_length = int(request.headers["content-length"])
            if content_length <= self._request_max_size:
                body = await request.body()
                await self._set_record_request_body(request, body)
                access_log += f" body: {body.decode()}"
            else:
                access_log += f" body: {content_length} bytes"
        else:
            access_log += " body: 0 bytes"
        return access_log

    async def _record_request(self, request: Request):
        logger.info(f"<api-record> request.headers: {request.headers}")
        access_log = f"<api-record> request record:{get_client_addr(request.scope)} - \"{request.method} {get_path_with_query_string(request.scope)} HTTP/{request.scope['http_version']}\""
        access_log = await self._record_request_body(access_log, request)
        logger.info(access_log)
        return request

    async def _record_response(self, start_time: float, response: Response):
        if "content-length" in response.headers:
            content_length = int(response.headers["content-length"])
            if content_length <= self._response_max_size:
                res_body = b""
                async for chunk in response.body_iterator:
                    res_body += chunk
                response = Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
                record = res_body.decode()
            else:
                record = f"{content_length} bytes"
        else:
            record = f"0 bytes"
        logger.info(f"<api-record> response: {record}, cost: {time.time() - start_time}")
        return response

    async def dispatch(self, request, call_next):
        start_time = time.time()
        request = await self._record_request(request)
        response = await call_next(request)
        response = await self._record_response(start_time, response)
        return response
    