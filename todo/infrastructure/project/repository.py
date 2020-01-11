import typing
from google.cloud import datastore

from todo.application.project.repository import ProjectRepository
from todo.domain.project import Project, ProjectKey, ProjectName

datastore_client = datastore.Client()


class DatastoreProjectRepository(ProjectRepository):
    def save(self, project: Project):
        key = datastore_client.key(project.key.KIND, project.key.project_id)
        entity = datastore.Entity(key)
        entity.update({
            "name": project.name.value,
            "created_at": project.created_at,
        })
        datastore_client.put(entity)

    def delete(self, key: ProjectKey):
        datastore_key = datastore_client.key(key.KIND, key.project_id)
        datastore_client.delete(datastore_key)

    def fetch_no_raise(self, key: ProjectKey) -> typing.Optional[Project]:
        datastore_key = datastore_client.key(key.KIND, key.project_id)
        doc = datastore_client.get(key=datastore_key)
        if doc is None:
            return None

        return self._to_domain_entity(doc=doc)

    def _to_domain_entity(self, doc: datastore.Entity) -> Project:
        return Project(
            key=ProjectKey.build_from_key(key=doc.key),
            name=ProjectName(doc["name"]),
            created_at=doc["created_at"],
        )

    def fetch_list(self) -> typing.List[Project]:
        query = datastore_client.query(kind=ProjectKey.KIND)
        projects = [
            self._to_domain_entity(doc=doc)
            for doc in query.fetch()
        ]

        return projects
