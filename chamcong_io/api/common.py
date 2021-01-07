from typing import List
from pydantic import BaseModel


class Response(BaseModel):
    status: str = None
    message: str = None
    

class Kafka(BaseModel):
    topic: str
    group_id: str = None
    brokers: List[str] 
    