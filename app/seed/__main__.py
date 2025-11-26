import asyncio
from .core import seed_core
if __name__=="__main__":
    asyncio.run(seed_core())

# uv run alembic upgrade head
# uv run python -m app.seed
