from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from common.response import SuccessResponse
from core.db import SessionLocal
from resources.schema import (
    AgResourceCreateSchema,
    AgResourceQuerySchema,
    AgResourceUpdateSchema,
    BatchSetStatus,
)
from resources.service import AgResourceService

AgResourceRouter = APIRouter(prefix="/v1/agno_manage/resources", tags=["资源管理"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@AgResourceRouter.get("/detail/{id}", summary="获取资源详情")
async def get_resource_detail(
    id: int = Path(..., description="ID"),
    db: Session = Depends(get_db),
) -> JSONResponse:
    result = await AgResourceService.detail(db=db, id=id)
    return SuccessResponse(data=result, msg="获取资源详情成功")


@AgResourceRouter.get("/list", summary="查询资源列表")
async def get_resource_list(
    query: AgResourceQuerySchema = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    result = await AgResourceService.page(db=db, query=query)
    return SuccessResponse(data=result, msg="查询资源列表成功")


@AgResourceRouter.post("/create", summary="创建资源")
async def create_resource(
    data: AgResourceCreateSchema,
    db: Session = Depends(get_db),
) -> JSONResponse:
    result = await AgResourceService.create(db=db, data=data)
    return SuccessResponse(data=result, msg="创建资源成功")


@AgResourceRouter.put("/update/{id}", summary="修改资源")
async def update_resource(
    data: AgResourceUpdateSchema,
    id: int = Path(..., description="ID"),
    db: Session = Depends(get_db),
) -> JSONResponse:
    result = await AgResourceService.update(db=db, id=id, data=data)
    return SuccessResponse(data=result, msg="修改资源成功")


@AgResourceRouter.delete("/delete", summary="批量删除资源")
async def delete_resource(
    ids: list[int] = Body(..., description="ID列表"),
    db: Session = Depends(get_db),
) -> JSONResponse:
    await AgResourceService.delete(db=db, ids=ids)
    return SuccessResponse(msg="删除资源成功")


@AgResourceRouter.patch("/status", summary="批量修改资源状态")
async def set_resource_status(
    data: BatchSetStatus,
    db: Session = Depends(get_db),
) -> JSONResponse:
    await AgResourceService.set_status(db=db, ids=data.ids, status=data.status)
    return SuccessResponse(msg="修改资源状态成功")
