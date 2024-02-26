from fastapi import FastAPI, Request, Response, HTTPException, APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/healthz",
    tags=['healthz']
)


@router.get("/")
async def check_database_connection(request: Request):
    # TODO: Add a return code for 503
    data = await request.body()
    if request.query_params or data:
        print("hello")
        return Response(status_code=400, headers={"Cache-Control": "no-cache"})
    else:
        return Response(status_code=200, headers={"Cache-Control": "no-cache"})

@router.post("/")
@router.delete("/")
@router.put("/")
@router.patch("/")
@router.head("/")
@router.options("/")
async def disallowed_methods(request: Request):
    return Response(status_code=405)

