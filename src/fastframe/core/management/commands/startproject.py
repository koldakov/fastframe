from fastframe.core.management._base import BaseCommand


class Command(BaseCommand):
    help = "Creates a FastFrame project directory structure."

    def handle(self, project_name: str) -> int:
        raise NotImplementedError()
