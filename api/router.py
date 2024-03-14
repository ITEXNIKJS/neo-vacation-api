from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")  # route_class=ServerErrorWrapperRoute)

from fastapi import APIRouter
from tours import *

router = APIRouter(prefix="/api/v1")  # route_class=ServerErrorWrapperRoute)

router.add_api_route(
    "/get_smth",
    get_tours,
    methods=["GET"]
)
