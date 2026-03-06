from pydantic import BaseModel

from app.schemas.edges import EdgeResponse
from app.schemas.nodes import NodeResponse


class NodePosition(BaseModel):
    id: str
    x: float
    y: float


class CanvasSaveRequest(BaseModel):
    node_positions: list[NodePosition] = []
    viewport: dict = {}


class CanvasStateResponse(BaseModel):
    nodes: list[NodeResponse]
    edges: list[EdgeResponse]
    viewport: dict
