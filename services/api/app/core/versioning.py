from datetime import datetime
from functools import wraps

from fastapi import Response


def deprecated(sunset_date: str, alternative: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract response object if injected
            response: Response = kwargs.get('response')
            if response:
                response.headers["Deprecation"] = "true"
                response.headers["Sunset"] = sunset_date
                response.headers["Link"] = f'<{alternative}>; rel="alternate"'
            return await func(*args, **kwargs)
        return wrapper
    return decorator
