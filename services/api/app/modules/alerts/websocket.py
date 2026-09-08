from __future__ import annotations

"""
services/api/app/modules/alerts/websocket.py
============================================
WebSocket connection manager for real-time alert delivery.
"""

import asyncio
import logging


import orjson
from fastapi import WebSocket, WebSocketDisconnect
from redis.asyncio.client import Redis

from app.auth.jwt_service import JWTService
from app.core.config import get_settings

logger = logging.getLogger("xaiguard.websocket")


class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages from Redis Pub/Sub.
    """

    def __init__(self):
        # Maps connection_id (str) to WebSocket object
        self.active_connections: dict[str, WebSocket] = {}
        # Maps connection_id to its listener Task
        self.listener_tasks: dict[str, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket, token: str, redis: Redis) -> str | None:
        """
        Authenticate and accept the WebSocket connection.
        Starts a background task to listen to Redis for this client.
        """
        await websocket.accept()
        
        # 1. Authenticate
        settings = get_settings()
        jwt_service = JWTService(
            secret_key=settings.SECRET_KEY.get_secret_value(),
            algorithm=settings.ALGORITHM
        )
        try:
            payload = jwt_service.verify_access_token(token)
            user_id = payload.sub
        except Exception as e:
            logger.warning(f"WebSocket auth failed: {e}")
            await websocket.close(code=4001, reason="Invalid authentication credentials")
            return None
            
        connection_id = f"{user_id}_{id(websocket)}"
        self.active_connections[connection_id] = websocket
        
        # 2. Start listener task
        task = asyncio.create_task(self._listen_redis(connection_id, redis))
        self.listener_tasks[connection_id] = task
        
        logger.info(f"WebSocket connected: {connection_id}")
        return connection_id

    async def disconnect(self, connection_id: str):
        """Clean up the connection and listener task."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            
        if connection_id in self.listener_tasks:
            self.listener_tasks[connection_id].cancel()
            del self.listener_tasks[connection_id]
            
        logger.info(f"WebSocket disconnected: {connection_id}")

    async def _listen_redis(self, connection_id: str, redis: Redis):
        """
        Background task: subscribes to Redis alerts and forwards them to the client.
        Includes slow-client protection (drops message if send blocks > 100ms).
        """
        pubsub = redis.pubsub()
        await pubsub.subscribe("xaiguard:alerts:live")
        
        websocket = self.active_connections.get(connection_id)
        if not websocket:
            return

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    payload = message["data"]
                    if isinstance(payload, bytes):
                        payload = payload.decode('utf-8')
                        
                    try:
                        # Send with a strict timeout to protect against slow clients
                        await asyncio.wait_for(
                            websocket.send_text(payload),
                            timeout=0.1
                        )
                    except asyncio.TimeoutError:
                        logger.warning(f"Slow client {connection_id}: Dropped alert message")
                    except WebSocketDisconnect:
                        break
        except asyncio.CancelledError:
            pass # Task was cancelled during disconnect
        except Exception as e:
            logger.error(f"Redis listener error for {connection_id}: {e}")
        finally:
            await pubsub.unsubscribe("xaiguard:alerts:live")
            await pubsub.close()

manager = ConnectionManager()

