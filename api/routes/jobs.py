from fastapi import APIRouter

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.get("/")
def list_jobs():
    return {
        "message": "Coming in Day 24"
    }