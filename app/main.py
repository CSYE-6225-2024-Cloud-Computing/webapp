from fastapi import FastAPI, Response, Request
from dotenv import load_dotenv
load_dotenv()

from . import models
import os
from .database import engine
from .routers import user, authenticated, healthz


models.Base.metadata.create_all(engine)
print("Database created successfully")

app = FastAPI()

print("============================== ROUTER: user.py================================")
app.include_router(user.router)


print("============================== ROUTER: authenticated.py================================")
app.include_router(authenticated.router)


print("============================== ROUTER: healthz.py================================")
app.include_router(healthz.router)



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)








