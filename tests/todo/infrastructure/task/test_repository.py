import main
import datetime
from google.cloud import datastore

from todo.application.task.repository import TaskRepository
from todo.domain.task import Task, TaskKey, TaskName

datastore_client = datastore.Client()


class TestTaskRepository:
    KIND = "Task"
    repository: TaskRepository = main.injector.get(TaskRepository)

    def test_save(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        task = Task(
            key=TaskKey.build_by_id(task_id=123),
            name=TaskName("Task Name"),
            finished_at=None,
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
            updated_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(task=task)
        assert len(list(query.fetch())) == 1

    def test_save_and_fetch(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        task = Task(
            key=TaskKey.build_by_id(task_id=123),
            name=TaskName("Task Name"),
            finished_at=None,
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
            updated_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(task=task)
        fetched_task = self.repository.fetch(key=task.key)
        assert fetched_task == task
