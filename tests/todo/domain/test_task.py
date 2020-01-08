import datetime
import pytest

from google.cloud import datastore
from dataclass_type_validator import TypeValidationError

from todo.domain.task import Task, TaskName


client = datastore.Client()


class TestTask:
    def test_build_successful(self):
        task = Task(
            key=client.key("Task", id=1),
            name=TaskName("Task Name"),
            finished_at=None,
            created_at=datetime.datetime(
                2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            updated_at=datetime.datetime(
                2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        assert isinstance(task, Task)

    def test_build_failure(self):
        with pytest.raises(expected_exception=TypeValidationError):
            Task(
                key=client.key("Task", id=1),
                name='task name',
                finished_at=None,
                created_at=datetime.datetime(
                    2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
                updated_at=datetime.datetime(
                    2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
            )
