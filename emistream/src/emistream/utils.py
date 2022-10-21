from asyncio import AbstractEventLoop, get_running_loop
from concurrent.futures import Executor
from functools import partial
from typing import TypeVar, Callable, Optional
from uuid import uuid4

T = TypeVar("T")


def generate_uuid() -> str:
    return uuid4().hex


async def background(
    f: Callable[..., T],
    *args,
    _loop: Optional[AbstractEventLoop] = None,
    _executor: Optional[Executor] = None,
    **kwargs,
) -> T:
    _loop = _loop or get_running_loop()
    f = partial(f, *args, **kwargs)
    return await _loop.run_in_executor(_executor, f)
