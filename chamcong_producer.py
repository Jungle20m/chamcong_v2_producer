import uvicorn
from fastapi import FastAPI

from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    application = FastAPI(title="discovery", version="2.0")
    # event handler: start and stop service
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    
    # application.include_router(discovery_router, prefix="/chamcong/producer")
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("chamcong_producer:app", host="0.0.0.0", port=7100, reload=True)