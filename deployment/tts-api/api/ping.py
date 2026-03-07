from fastapi import APIRouter, Request

ping_router = APIRouter(
    prefix="/ping",
    tags=["ping"],
)


@ping_router.get("/")
def pong(request: Request):
    print("My Header: ", request.headers)
    print("Text debug")
    return {"message": "pong!"}
