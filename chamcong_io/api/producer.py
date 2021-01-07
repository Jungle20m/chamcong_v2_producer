from typing import List
from pydantic import BaseModel

from .common import Response, Kafka


class Camera(BaseModel):
    id: str
    resource: str 


class DataConfig(BaseModel):
    camera: Camera
    producer: Kafka


class ResponseConfig(Response):
    data: List[DataConfig] = []