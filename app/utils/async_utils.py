# app/utils/async_utils.py
import asyncio


async def run_with_timeout(coro, timeout: float):
    """
    코루틴을 timeout 내 실행. 초과 시 TimeoutError 발생
    """
    return await asyncio.wait_for(coro, timeout=timeout)


def run_sync(async_fn, *args, **kwargs):
    """
    async 함수 sync에서 실행하는 wrapper
    """
    return asyncio.run(async_fn(*args, **kwargs))
