from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class AgResourceCreateSchema(BaseModel):
    name: str = Field(..., max_length=255, description='资源名称')
    category: str = Field(..., description='资源大类(model/embedder/reader/toolkit/knowledge/agent/team等)')
    type: str = Field(..., description='具体类型(openai/pdf/duckduckgo/base等)')
    config: dict = Field(default_factory=dict, description='资源配置')
    status: str = Field(default="0", description='状态(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='描述')


class AgResourceUpdateSchema(AgResourceCreateSchema):
    pass


class AgResourceOutSchema(AgResourceCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime


class BatchSetStatus(BaseModel):
    ids: list[int] = Field(..., description='ID列表')
    status: str = Field(..., description='目标状态(0:启用 1:禁用)')


class AgResourceQuerySchema:
    def __init__(
        self,
        name: str | None = Query(None, description='资源名称（模糊匹配）'),
        category: str | None = Query(None, description='资源大类'),
        type: str | None = Query(None, description='具体类型'),
        status: str | None = Query(None, description='状态(0:启用 1:禁用)'),
        page: int = Query(1, ge=1, description='页码'),
        page_size: int = Query(20, ge=1, le=100, description='每页数量'),
    ) -> None:
        self.name = name
        self.category = category
        self.type = type
        self.status = status
        self.page = page
        self.page_size = page_size
