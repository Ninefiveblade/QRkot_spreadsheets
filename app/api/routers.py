from fastapi import APIRouter

from app.api.endpoints import donate_router, charity_router, user_router, google_api_router

main_router = APIRouter()
main_router.include_router(
    donate_router, prefix='/donation', tags=['donations'],
)
main_router.include_router(
    charity_router, prefix='/charity_project', tags=['charity_projects']
)
main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)
main_router.include_router(user_router)