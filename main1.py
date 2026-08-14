from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/slow-async")
async def slow_async():
    # async 방식의 대기시간 측정
    await asyncio.sleep(3)  # 3초 대기 (기다리는 동안 다른 작업 가능)
    return {"type": "async","message": "3초 대기 완료"}

@app.get("/slow-block")
async def slow_block():
    # sync 방식의 대기시간 측정
    time.sleep(3)  # 3초 동안 완전히 멈춤
    return {"type": "block","message": "3초 대기 완료"}
