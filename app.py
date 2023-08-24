from starlette.middleware.cors import CORSMiddleware
from bootstrap_config import bootstrap_config, app_config
from fastapi import FastAPI, Request, Response, HTTPException
from controller import users, auth, uploads, validate, schema
import traceback
import os
import uvicorn
from fastapi import FastAPI
from loguru import logger
import sentry_sdk
import logging
from utils.mongo import get_mongo

logger.add("logs/{time}.log", rotation="1 day",
           retention="10 days", level="INFO")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = [InterceptHandler()]

if os.environ.get("ENV", "development") == "production":
    sentry_sdk.init(
        dsn="https://ebb72b75b745eab8f4aa196844519122@o4505628567404544.ingest.sentry.io/4505628572516352",
        traces_sample_rate=1.0,
    )


if (app_config.get("DATABASE_URL") is None):
    bootstrap_config()

mainApp = FastAPI()


def catch_exceptions_middleware(request: Request, call_next):
    try:
        return call_next(request)
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception:
        traceback.print_exc()
        return Response("Internal server error", status_code=500)


def setup_main_app():
    mainApp.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    mainApp.include_router(users.router)
    mainApp.include_router(auth.router)
    mainApp.include_router(validate.router)
    mainApp.include_router(uploads.router)
    mainApp.include_router(schema.router)
    mainApp.middleware("http")(catch_exceptions_middleware)


app = FastAPI()


@app.get(
    path="/health", description="Health check"
)
def health_check():
    return {"status": "OK"}


app.mount("/", mainApp)


setup_main_app()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)
