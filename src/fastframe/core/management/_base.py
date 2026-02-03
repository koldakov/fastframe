from __future__ import annotations

import inspect
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, TextIO


class BaseCommand(ABC):
    """
    Base class for commands.

    Attributes:
      - help (str): short description.
      - deprecated (bool): deprecated.
    """

    name: str = ""
    help: ClassVar[str] = ""
    deprecated: bool = False

    stdout: ClassVar[TextIO] = sys.stdout

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if not cls.name:
            cls.name = Path(inspect.getfile(cls)).stem

    @abstractmethod
    def handle(self, *args, **kwargs) -> int:
        """Execute the command."""
