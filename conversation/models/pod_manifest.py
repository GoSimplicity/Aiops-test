from pydantic import BaseModel, Field
from typing import List, Optional


class ContainerSpec(BaseModel):
    name: str
    image: str
    ports: Optional[List[dict]] = None


class PodSpec(BaseModel):
    containers: List[ContainerSpec]


class Metadata(BaseModel):
    name: str
    labels: Optional[dict] = None


class PodManifest(BaseModel):
    apiVersion: str = Field(default="v1")
    kind: str = Field(default="Pod")
    metadata: Metadata
    spec: PodSpec
