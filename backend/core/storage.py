from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4


class Storage(ABC):
    """文件存储抽象接口。"""

    @abstractmethod
    def save(self, file: BinaryIO, filename: str) -> str:
        """保存文件，返回相对路径。"""
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        """删除文件。"""
        pass

    @abstractmethod
    def get_url(self, path: str) -> str:
        """获取访问 URL。"""
        pass


class LocalStorage(Storage):
    """本地文件系统存储。"""

    def __init__(self, base_dir: str = "./uploads"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, file: BinaryIO, filename: str) -> str:
        """按日期分目录存储：YYYY/MM/DD/uuid_filename。"""
        date_path = datetime.now().strftime("%Y/%m/%d")
        dir_path = self.base_dir / date_path
        dir_path.mkdir(parents=True, exist_ok=True)

        file_path = dir_path / f"{uuid4().hex}_{filename}"
        with open(file_path, "wb") as f:
            f.write(file.read())

        return str(file_path.relative_to(self.base_dir))

    def delete(self, path: str) -> None:
        """删除文件，不存在不报错。"""
        (self.base_dir / path).unlink(missing_ok=True)

    def get_url(self, path: str) -> str:
        """返回相对 URL 路径。"""
        return f"/uploads/{path}"


# 全局单例
storage = LocalStorage()
