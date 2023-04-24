import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import trading_bot_router
app = FastAPI()

app.include_router(trading_bot_router.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Welcome"])
def welcome():
    return "Welcome to the Cryptocurrency Trading Bot API"


if __name__ == "__main__":
    uvicorn.run(app=app, host="192.168.0.207", port=6969)
    pass
