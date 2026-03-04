from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "agentcoin-api"}


@router.get("/ready")
def readiness_check():
    return {"ready": True}
