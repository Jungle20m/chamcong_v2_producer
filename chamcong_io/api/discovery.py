from typing import List, Optional
from pydantic import BaseModel

from .producer import ProducerConfig


class KafkaConfig(BaseModel):
    topic: str
    group_id: str
    bootstrap_servers: List[str]


class ResponseProducerConfigInfo(BaseModel):
    data: List[ProducerConfig]