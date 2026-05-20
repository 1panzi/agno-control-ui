from fastapi import APIRouter

from resources.controller import AgResourceRouter
from catalog.controller import CatalogRouter
from api.v1.debug import DebugRouter

router = APIRouter(prefix="/api")

router.include_router(AgResourceRouter)
router.include_router(CatalogRouter)
router.include_router(DebugRouter)
