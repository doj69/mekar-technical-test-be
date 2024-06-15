import logging
import re
import time
import uuid
from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from core import utils

logger = logging.getLogger(__name__)
request_id = None


class HTTPRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            api_route = self.__get_api_route(request)
            route_path = api_route.path if api_route else None
            http_request = dict()
            global request_id
            request_id = str(uuid.uuid4())
            start_time = time.time()
            ip = utils.get_ip_address(request)
            if request.url.path != "/healthcheck":
                http_request.update(
                    {
                        "requestMethod": request.method,
                        "requestUrl": str(request.url),
                        "requestSize": request.headers.get("Content-Length", 0),
                        "userAgent": request.headers.get("User-Agent"),
                        "remoteIp": ip,
                        "client": request.client,
                        "request": {
                            "id": request_id,
                            "route": route_path,
                        },
                    }
                )

                logger.info(
                    f"incoming request-{request_id}",
                    extra={
                        "httpRequest": http_request,
                        "spanId": request_id,
                    },
                )

            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)
            response.headers["X-Process-Time"] = f"{formatted_process_time} ms"
            http_request.update(
                {
                    "requestMethod": request.method,
                    "requestUrl": str(request.url),
                    "requestSize": request.headers.get("Content-Length", 0),
                    "status": response.status_code,
                    "responseSize": response.headers.get("Content-Length"),
                    "userAgent": request.headers.get("User-Agent"),
                    "remoteIp": ip,
                    "client": request.client,
                    "latency": f"{formatted_process_time}ms",
                    "request": {
                        "id": request_id,
                        "route": route_path,
                    },
                }
            )

            if request.url.path != "/healthcheck":
                logger.info(
                    f"complete request-{request_id}",
                    extra={
                        "httpRequest": http_request,
                        "spanId": request_id,
                    },
                )

            return response
        except Exception as e:
            logger.exception(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "error_code": "error.internal_server_error",
                },
            )

    def __get_api_route(self, request: Request) -> Optional[APIRoute]:
        # Get the request path (excluding query parameters) and method
        request_path = request.url.path
        request_method = request.method

        # Find the corresponding APIRoute object by matching the request path and method
        matching_route = None
        for route in request.app.routes:
            # Modify the route path to create a regex pattern that ignores type annotations
            pattern = route.path
            # Replace path parameters with regex patterns, removing type hints
            pattern = re.sub(r"{(\w+):\s*\w+}", r"{\1}", pattern)
            # Convert the modified path to a regex pattern
            path_regex = re.compile(
                "^" + pattern.replace("{", "(?P<").replace("}", ">[^/]+)") + "$"
            )
            if path_regex.match(request_path) and request_method in route.methods:
                matching_route = route
                break

        return matching_route
