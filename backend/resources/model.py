from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base, EntityMixin


class AgResourceModel(Base, EntityMixin):
    __tablename__ = 'ag_resources'
    __table_args__ = {'comment': 'AI资源统一管理表'}

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment='资源名称')
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
        comment='资源大类(model/embedder/reader/toolkit/knowledge/agent/team等)'
    )
    type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
        comment='具体类型(openai/pdf/duckduckgo/base等)'
    )
    config: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict,
        comment='资源配置（支持ref引用或inline内联）'
    )
