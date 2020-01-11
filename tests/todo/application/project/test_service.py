import main
from google.cloud import datastore

from todo.application.project.repository import ProjectRepository
from todo.application.project import ProjectCreateService
from todo.domain.project import ProjectKey

datastore_client = datastore.Client()


class TestProjectService:
    KIND = ProjectKey.KIND
    repository: ProjectRepository = main.injector.get(ProjectRepository)

    def test_create_service(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        project_name = "ProjectName"
        service = main.injector.get(ProjectCreateService)
        service.execute(project_name=project_name)

        assert len(list(query.fetch())) == 1
