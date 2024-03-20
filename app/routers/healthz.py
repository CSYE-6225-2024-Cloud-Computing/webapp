from fastapi import FastAPI, Request, Response, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import logging
from pythonjsonlogger import jsonlogger



router = APIRouter(
    prefix="/healthz",
    tags=['healthz']
)

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create JSON handler with log file path
log_file_path = './webapp.log'  # Specify the log file path here
logHandler = logging.FileHandler(log_file_path)
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


@router.get("/")
async def check_database_connection(request: Request):
    # TODO: Add a return code for 503
    data = await request.body()
    if request.query_params or data:
        logger.warning("Unexpected query parameters or body data received")
        return Response(status_code=400, headers={"Cache-Control": "no-cache"})
    else:
        logger.info("Health check endpoint accessed successfully")
        return Response(status_code=200, headers={"Cache-Control": "no-cache"})

@router.post("/")
@router.delete("/")
@router.put("/")
@router.patch("/")
@router.head("/")
@router.options("/")
async def disallowed_methods(request: Request):
    logger.warning("Disallowed HTTP method called")
    return Response(status_code=405)

