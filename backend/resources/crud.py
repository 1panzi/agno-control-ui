from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from resources.model import AgResourceModel
from resources.schema import AgResourceCreateSchema, AgResourceUpdateSchema


class AgResourceCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, id: int) -> AgResourceModel | None:
        return self.db.get(AgResourceModel, id)

    def get_by_uuid(self, uuid: str) -> AgResourceModel | None:
        return self.db.execute(
            select(AgResourceModel).where(AgResourceModel.uuid == uuid)
        ).scalar_one_or_none()

    def list_enabled(self, category: str | None = None) -> list[AgResourceModel]:
        stmt = select(AgResourceModel).where(AgResourceModel.status == "0")
        if category:
            stmt = stmt.where(AgResourceModel.category == category)
        return list(self.db.execute(stmt).scalars().all())

    def page(
        self,
        page: int,
        page_size: int,
        name: str | None = None,
        category: str | None = None,
        type: str | None = None,
        status: str | None = None,
    ) -> dict:
        stmt = select(AgResourceModel)
        count_stmt = select(func.count()).select_from(AgResourceModel)

        if name:
            stmt = stmt.where(AgResourceModel.name.like(f"%{name}%"))
            count_stmt = count_stmt.where(AgResourceModel.name.like(f"%{name}%"))
        if category:
            stmt = stmt.where(AgResourceModel.category == category)
            count_stmt = count_stmt.where(AgResourceModel.category == category)
        if type:
            stmt = stmt.where(AgResourceModel.type == type)
            count_stmt = count_stmt.where(AgResourceModel.type == type)
        if status:
            stmt = stmt.where(AgResourceModel.status == status)
            count_stmt = count_stmt.where(AgResourceModel.status == status)

        total = self.db.execute(count_stmt).scalar() or 0
        offset = (page - 1) * page_size
        rows = list(self.db.execute(stmt.offset(offset).limit(page_size)).scalars().all())
        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_next": offset + page_size < total,
            "items": rows,
        }

    def create(self, data: AgResourceCreateSchema) -> AgResourceModel:
        obj = AgResourceModel(**data.model_dump())
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, data: AgResourceUpdateSchema) -> AgResourceModel | None:
        obj = self.get_by_id(id)
        if obj is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, ids: list[int]) -> None:
        self.db.execute(delete(AgResourceModel).where(AgResourceModel.id.in_(ids)))
        self.db.flush()

    def set_status(self, ids: list[int], status: str) -> None:
        self.db.execute(
            update(AgResourceModel)
            .where(AgResourceModel.id.in_(ids))
            .values(status=status)
        )
        self.db.flush()
