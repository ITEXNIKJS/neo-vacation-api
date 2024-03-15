from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")  # route_class=ServerErrorWrapperRoute)

# router.add_api_route(
#     "/get_tours",
#     get_tours,
#     methods=["GET"]
# )
