import typing
from google.cloud import datastore

from todo.application.task.repository import TaskRepository
from todo.domain.task import Task, TaskKey, TaskName

datastore_client = datastore.Client()


class DatastoreTaskRepository(TaskRepository):
    def save(self, task: Task):
        key = datastore_client.key(task.key.KIND, task.key.task_id)
        entity = datastore.Entity(key)
        entity.update({
            "name": task.name.value,
            "finished_at": task.finished_at,
            "created_at": task.created_at,
            "update_at": task.updated_at,
        })
        datastore_client.put(entity)

    def delete(self, key: TaskKey):
        datastore_key = datastore_client.key(key.KIND, key.task_id)
        datastore_client.delete(datastore_key)

    def fetch_no_raise(self, key: TaskKey) -> typing.Optional[Task]:
        datastore_key = datastore_client.key(key.KIND, key.task_id)
        doc = datastore_client.get(key=datastore_key)
        if doc is None:
            return None

        return self._to_domain_entity(doc=doc)

    def _to_domain_entity(self, doc: datastore.Entity) -> Task:
        return Task(
            key=TaskKey.build_from_key(key=doc.key),
            name=TaskName(doc["name"]),
            finished_at=doc["finished_at"],
            created_at=doc["created_at"],
            updated_at=doc["update_at"],
        )

    def fetch_list(self) -> typing.List[Task]:
        query = datastore_client.query(kind=TaskKey.KIND)
        tasks = [
            self._to_domain_entity(doc=doc)
            for doc in query.fetch()
        ]

        return tasks
