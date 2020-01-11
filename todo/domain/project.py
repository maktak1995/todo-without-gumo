import dataclasses
import datetime
import re
import base64
import uuid
from typing import Union
from google.cloud import datastore

from dataclass_type_validator import dataclass_type_validator


@dataclasses.dataclass(frozen=True)
class ProjectKey:
    _project_id: Union[str, int]
    KIND = "Project"

    @classmethod
    def build_by_id(cls, project_id: int) -> "ProjectKey":
        if isinstance(project_id, str) and project_id.isdigit():
            project_id = int(project_id)
        return cls(_project_id=project_id)

    @classmethod
    def build_for_new(cls) -> "ProjectKey":
        return cls(_project_id=cls._generate_new_uuid())

    @classmethod
    def build_from_key(cls, key: datastore.key) -> "ProjectKey":
        if key.parent:
            raise ValueError(f"key must not have parent")
        if key.kind != cls.KIND:
            raise ValueError(f"key.KIND must equal to {cls.KIND}: {key.kind}")

        return cls.build_by_id(project_id=key.id_or_name)

    @classmethod
    def _generate_new_uuid(cls) -> Union[str, int]:
        s: Union[str, int] = base64.b32encode(uuid.uuid4().bytes).decode('utf-8')
        return s.replace('======', '').lower()

    @property
    def project_id(self) -> int:
        return self._project_id


@dataclasses.dataclass(frozen=True)
class ProjectName:  # TaskのKey構造と生成メソッドの定義
    value: str

    MAX_LENGTH = 100

    def __post_init__(self):
        dataclass_type_validator(self)

        if len(self.value) == 0:
            raise ValueError(f"TaskName must be present.")

        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"TaskName is too long (maximum length is {self.MAX_LENGTH})")

        if re.fullmatch(r'\s', self.value):
            raise ValueError(f"Only space character cannot be used as TaskName")


@dataclasses.dataclass(frozen=True)
class Project:
    key: ProjectKey
    name: ProjectName
    created_at: datetime.datetime

    def __post_init__(self):
        dataclass_type_validator(self)
