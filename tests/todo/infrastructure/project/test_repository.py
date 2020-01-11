import main
import datetime
from google.cloud import datastore

from todo.application.project.repository import ProjectRepository
from todo.domain.project import Project, ProjectKey, ProjectName

datastore_client = datastore.Client()


class TestProjectRepository:
    KIND = ProjectKey.KIND
    repository: ProjectRepository = main.injector.get(ProjectRepository)

    def test_save(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        project = Project(
            key=ProjectKey.build_by_id(project_id=123),
            name=ProjectName("Project Name"),
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(project=project)
        assert len(list(query.fetch())) == 1

    def test_save_and_fetch(self):
        query = datastore_client.query(kind=self.KIND)
        query.keys_only()
        datastore_client.delete_multi(keys=[entity.key for entity in query.fetch()])
        assert len(list(query.fetch())) == 0

        project = Project(
            key=ProjectKey.build_by_id(project_id=123),
            name=ProjectName("Project Name"),
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(project=project)
        fetched_project = self.repository.fetch(key=project.key)
        assert fetched_project == project
