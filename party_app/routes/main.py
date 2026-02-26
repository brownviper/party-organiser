from fastapi import APIRouter

from party_app.routes import party_list


api_router = APIRouter()

api_router.include_router(party_list.router)
