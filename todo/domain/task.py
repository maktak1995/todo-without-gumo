import dataclasses
import datetime
import re
import base64
import uuid
from typing import Optional

from dataclass_type_validator import dataclass_type_validator


@dataclasses.dataclass(frozen=True)
class TaskKey:
    _task_id: int
    _kind: str = "Task"

    @classmethod
    def build_by_id(cls, task_id: int) -> "TaskKey":
        if isinstance(task_id, str) and task_id.isdigit():
            task_id = int(task_id)
        return cls(_task_id=task_id)

    @classmethod
    def build_for_new(cls) -> "TaskKey":
        return cls(_task_id=int(cls._generate_new_uuid()))

    @classmethod
    def _generate_new_uuid(cls) -> str:
        s = base64.b32encode(uuid.uuid4().bytes).decode('utf-8')
        return s.replace('======', '').lower()

    @property
    def task_id(self) -> int:
        return self._task_id


@dataclasses.dataclass(frozen=True)
class TaskName:  # TaskのKey構造と生成メソッドの定義
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
class Task:
    key: TaskKey
    name: TaskName
    finished_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __post_init__(self):
        dataclass_type_validator(self)

    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None

    def _clone(self, **changes) -> "Task":
        return dataclasses.replace(
            self,
            updated_at=datetime.datetime.utcnow().astimezone(tz=datetime.timezone.utc),
            **changes
        )

    def with_finished_at(self, finished_at: datetime.datetime) -> "Task":
        return self._clone(finished_at=finished_at)

    def to_canceled_finish(self) -> "Task":
        return self._clone(finished_at=None)

    def to_finished_now(self) -> "Task":
        return self.with_finished_at(
            finished_at=datetime.datetime.utcnow().astimezone(tz=datetime.timezone.utc)
        )

    def to_changed_task_name(self, task_name: TaskName) -> "Task":
        return self._clone(name=task_name)
