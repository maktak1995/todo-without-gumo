import main
from google.cloud import datastore

from todo.application.task.repository import TaskRepository
from todo.application.task import TaskCreateService, TaskStatusUpdateService, TaskNameUpdateService
from todo.domain.task import TaskKey

datastore_client = datastore.Client()


class TestTaskService:
    KIND = "Task"
    repository: TaskRepository = main.injector.get(TaskRepository)

    def test_create_service(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        task_name = "TaskName"
        service = main.injector.get(TaskCreateService)
        service.execute(task_name=task_name)

        assert len(list(query.fetch())) == 1

    def test_status_update_service(self):
        task_name = "TaskName"
        create_service = main.injector.get(TaskCreateService)
        task = create_service.execute(task_name=task_name)

        status_update_service = main.injector.get(TaskStatusUpdateService)
        updated_task = status_update_service.execute(key=task.key, finished=True)

        assert updated_task.is_finished

    def test_task_name_update_service(self):
        task_name = "TaskName"
        create_service = main.injector.get(TaskCreateService)
        task = create_service.execute(task_name=task_name)

        task_name_update_service = main.injector.get(TaskNameUpdateService)
        updated_task = task_name_update_service.execute(key=task.key, task_name="NewTaskName")

        assert updated_task.name.value == "NewTaskName"
