from __future__ import annotations

import functools
import pkgutil
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Final, NamedTuple

import typer
from typer.models import CommandInfo

from fastframe.utils import metadata

if TYPE_CHECKING:
    from ._base import BaseCommand

_COMMANDS_DIR_NAME: Final[str] = "commands"


class CommandSpec(NamedTuple):
    name: str
    module_base: str


def _find_commands(management_dir: Path, /) -> list[str]:
    return [
        file_name
        for _, file_name, is_pkg in pkgutil.iter_modules([management_dir / _COMMANDS_DIR_NAME])
        if not is_pkg and not file_name.startswith("_")
    ]


def _get_app_commands() -> list[CommandSpec]:
    raise NotImplementedError()


def _get_core_commands() -> list[CommandSpec]:
    return [
        CommandSpec(name=command_name, module_base="fastframe.core")
        for command_name in _find_commands(Path(__file__).parent)
    ]


@functools.cache
def get_commands() -> list[CommandSpec]:
    return [
        *_get_core_commands(),
        *_get_app_commands(),
    ]


class ManagementUtility(typer.Typer):
    _management_dir_name: ClassVar[str] = "management"

    def __init__(self, **kwargs) -> None:
        super().__init__(
            **kwargs,
            help=f"{metadata['name']} management CLI.",
        )
        self._register_commands()

    def execute(self) -> int:
        self()
        return 0

    def _register_commands(self) -> None:
        for spec in get_commands():
            command: BaseCommand = self._load_command(spec)
            self._register_command(command)

    def _get_module_path(self, spec: CommandSpec, /) -> str:
        return f"{spec.module_base}.{self._management_dir_name}.{_COMMANDS_DIR_NAME}.{spec.name}"

    def _load_command(self, spec: CommandSpec, /) -> BaseCommand:
        return import_module(self._get_module_path(spec)).Command()

    def _register_command(self, command: BaseCommand, /) -> None:
        self.registered_commands.append(
            CommandInfo(
                name=command.name,
                callback=command.handle,
                help=command.help,
                deprecated=command.deprecated,
            )
        )


def execute_from_command_line() -> int:
    utility: ManagementUtility = ManagementUtility()
    return utility.execute()
