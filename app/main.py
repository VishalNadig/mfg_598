import os
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# from fastapi_pagination import add_pagination
# from fastapi_redis_cache import FastApiRedisCache
# from routes import (
#     admin_router,
#     # chatgpt_router,
#     chefbot_router,
#     math_router,
#     plutus,
#     # prefect_router,
#     robotics_router,
# )
# from sqlalchemy.orm import Session

# app = FastAPI()

# app.include_router(admin_router.router)
# app.include_router(chefbot_router.router)
# app.include_router(math_router.router)
# app.include_router(robotics_router.router)
# app.include_router(plutus.router)
# # app.include_router(chatgpt_router.router)
# # app.include_router(prefect_router.router)

# # add_pagination(app)
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/", tags=["Welcome"])
# def welcome():
#     return "Welcome master Vishal. I am Megamind"


if __name__ == "__main__":
    # uvicorn.run(app=app, host="192.168.0.207", port=6969)
    pass
