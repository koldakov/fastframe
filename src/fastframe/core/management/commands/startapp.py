from fastframe.core.management._base import BaseCommand


class Command(BaseCommand):
    help = "Creates a FastFrame app directory structure."

    def handle(self, app_name: str) -> int:
        raise NotImplementedError()
