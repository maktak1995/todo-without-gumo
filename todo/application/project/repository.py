import typing
from todo.domain.project import Project, ProjectKey


class ProjectRepository:
    def save(self, project: Project):
        raise NotImplementedError()

    def delete(self, key: ProjectKey):
        raise NotImplementedError()

    def fetch(self, key: ProjectKey):
        project = self.fetch_no_raise(key=key)
        if project is None:
            raise RuntimeError(f"Object Not Found")
        return project

    def fetch_no_raise(self, key: ProjectKey) -> typing.Optional[Project]:
        raise NotImplementedError()

    def fetch_list(self) -> typing.List[Project]:
        raise NotImplementedError()
