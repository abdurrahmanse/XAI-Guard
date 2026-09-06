import asyncio
import argparse
import sys
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import asyncpg
import httpx
import redis.asyncio as redis

console = Console()

async def check_postgres(url: str) -> bool:
    try:
        conn = await asyncpg.connect(url)
        await conn.fetchval('SELECT 1')
        await conn.close()
        return True
    except Exception:
        return False

async def check_redis(url: str) -> bool:
    try:
        r = redis.from_url(url)
        res = await r.ping()
        await r.aclose()
        return res
    except Exception:
        return False

async def check_http(url: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(url)
            return resp.status_code == 200
    except Exception:
        return False

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait", type=int, default=0, help="Wait up to X seconds for services to become healthy")
    args = parser.parse_args()

    # Read from env or use defaults
    pg_url = "postgresql://postgres:password@localhost:5434/postgres"
    redis_url = "redis://localhost:6380/0"
    mlflow_url = "http://localhost:5500/api/2.0/mlflow/experiments/list"
    minio_url = "http://localhost:9000/minio/health/live"

    console.print("\n[bold blue]Checking XAI-Guard Infrastructure Health...[/bold blue]\n")

    start_time = time.time()
    wait_time = args.wait

    while True:
        pg_ok = await check_postgres(pg_url)
        redis_ok = await check_redis(redis_url)
        mlflow_ok = await check_http(mlflow_url)
        minio_ok = await check_http(minio_url)

        all_ok = pg_ok and redis_ok and mlflow_ok and minio_ok

        if all_ok:
            console.print(f"  [bold green]✓ PostgreSQL:[/bold green] Connected ({pg_url})")
            console.print(f"  [bold green]✓ Redis:[/bold green] Connected ({redis_url})")
            console.print(f"  [bold green]✓ MLflow:[/bold green] Connected ({mlflow_url})")
            console.print(f"  [bold green]✓ MinIO:[/bold green] Connected ({minio_url})")
            console.print("\n[bold green]All infrastructure services are healthy! 🚀[/bold green]\n")
            sys.exit(0)
        
        elapsed = time.time() - start_time
        if elapsed >= wait_time:
            console.print(f"  [{'bold green' if pg_ok else 'bold red'}]{'✓' if pg_ok else '✗'} PostgreSQL[/]")
            console.print(f"  [{'bold green' if redis_ok else 'bold red'}]{'✓' if redis_ok else '✗'} Redis[/]")
            console.print(f"  [{'bold green' if mlflow_ok else 'bold red'}]{'✓' if mlflow_ok else '✗'} MLflow[/]")
            console.print(f"  [{'bold green' if minio_ok else 'bold red'}]{'✓' if minio_ok else '✗'} MinIO[/]")
            console.print("\n[bold red]Health check failed. Some services are unreachable.[/bold red]\n")
            sys.exit(1)
        
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
