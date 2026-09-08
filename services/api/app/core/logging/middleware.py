import time
import uuid

from app.core.logging.logger import get_logger, request_id_var
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = get_logger(__name__)

class StructLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        token = request_id_var.set(req_id)
        
        start_time = time.time()
        logger.debug("Request started", method=request.method, url=str(request.url))
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info("Request completed", status_code=response.status_code, duration_s=duration)
            response.headers["X-Request-ID"] = req_id
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error("Request failed", error=str(e), duration_s=duration, exc_info=True)
            raise
        finally:
            request_id_var.reset(token)
