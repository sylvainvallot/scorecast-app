from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.get("/status")
async def status():
    return {"status": "ok"}
