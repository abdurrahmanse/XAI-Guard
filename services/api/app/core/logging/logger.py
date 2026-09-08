import logging
import uuid
from contextvars import ContextVar
from typing import Any, Dict

import structlog

# Context variables for tracing
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")

def add_context_vars(logger: logging.Logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    req_id = request_id_var.get()
    if req_id:
        event_dict["request_id"] = req_id
    
    uid = user_id_var.get()
    if uid:
        event_dict["user_id"] = uid
        
    event_dict["service"] = "xaiguard-api"
    return event_dict

def configure_logging(environment: str = "development"):
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_context_vars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if environment == "production":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    return structlog.get_logger(name)
