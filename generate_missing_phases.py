import os
import json

# 6.6 Structured Logging
os.makedirs('services/api/app/core/logging', exist_ok=True)

with open('services/api/app/core/logging/logger.py', 'w') as f:
    f.write("""import structlog
import logging
from contextvars import ContextVar
from typing import Any, Dict
import uuid

# Context variables for tracing
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")

def add_context_vars(logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
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
""")

with open('services/api/app/core/logging/middleware.py', 'w') as f:
    f.write("""import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging.logger import request_id_var, get_logger

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
""")

# 8.5 Dashboard Route Architecture
dash_app = 'apps/dashboard/src/app'
os.makedirs(f'{dash_app}/(auth)/login', exist_ok=True)
os.makedirs(f'{dash_app}/(dashboard)/alerts/[id]', exist_ok=True)
os.makedirs(f'{dash_app}/(dashboard)/metrics', exist_ok=True)
os.makedirs(f'{dash_app}/(dashboard)/models', exist_ok=True)

for path in [
    f'{dash_app}/(auth)/login',
    f'{dash_app}/(dashboard)',
    f'{dash_app}/(dashboard)/alerts',
    f'{dash_app}/(dashboard)/alerts/[id]',
    f'{dash_app}/(dashboard)/metrics',
    f'{dash_app}/(dashboard)/models'
]:
    with open(f'{path}/page.tsx', 'w') as f:
        f.write(f"""export default function Page() {{
  return <div>{path.split('/')[-1] if not path.endswith('(dashboard)') else 'Dashboard Live Feed'} Page</div>;
}}
""")

with open(f'{dash_app}/(dashboard)/layout.tsx', 'w') as f:
    f.write("""export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  // Real layout will include WebSocket context provider and server-component sidebar
  return (
    <div className="flex h-screen bg-background text-foreground">
      <aside className="w-64 border-r border-border">Sidebar</aside>
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  );
}
""")

# 8.6 Admin Panel Route Architecture
admin_app = 'apps/admin/src/app'
os.makedirs(f'{admin_app}/(auth)/login', exist_ok=True)
os.makedirs(f'{admin_app}/(admin)/experiments/[runId]', exist_ok=True)
os.makedirs(f'{admin_app}/(admin)/models', exist_ok=True)
os.makedirs(f'{admin_app}/(admin)/champion', exist_ok=True)
os.makedirs(f'{admin_app}/(admin)/reports', exist_ok=True)

for path in [
    f'{admin_app}/(auth)/login',
    f'{admin_app}/(admin)/experiments',
    f'{admin_app}/(admin)/experiments/[runId]',
    f'{admin_app}/(admin)/models',
    f'{admin_app}/(admin)/champion',
    f'{admin_app}/(admin)/reports'
]:
    with open(f'{path}/page.tsx', 'w') as f:
        f.write(f"""export default function Page() {{
  return <div>{path.split('/')[-1]} Admin Page</div>;
}}
""")

with open(f'{admin_app}/(admin)/layout.tsx', 'w') as f:
    f.write("""export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <header className="h-16 border-b border-border">Admin Topbar</header>
      <main className="flex-1 container mx-auto py-6">{children}</main>
    </div>
  );
}
""")

with open(f'{admin_app}/middleware.ts', 'w') as f:
    f.write("""import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Stub for JWT Role checking.
  // Analysts are redirected back to the dashboard if they attempt to access /admin
  const token = request.cookies.get('jwt');
  if (token && token.value === 'analyst-role-stub') {
    return NextResponse.redirect(new URL('http://localhost:3001')); // Dashboard URL
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
""")

print("Successfully generated missing Phase 6 and Phase 8 implementations.")
