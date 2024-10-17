import typing
from endstone._internal.endstone_python import Player

### Object Types ###


class SimpleFunctionality(typing.TypedDict):
    type: str
    content: str


class EasySlashCommand:
    def __init__(
        self,
        name: str,
        description: str,
        usages: list[str],
        permissions: list[str],
        aliases: list[str],
        functionality: list[SimpleFunctionality],
    ):
        self.name = name
        self.description = description
        self.usages = usages
        self.permissions = permissions
        self.aliases = aliases
        self.functionality = functionality


class EasyExecution:
    def __init__(
        self, name: str, callback: typing.Callable[[Player, str, list[str]], None]
    ):
        self.name = name
        self.callback = callback


class EasyCondition:
    def __init__(
        self, name: str, callback: typing.Callable[[Player, str, list[str]], bool]
    ):
        self.name = name
        self.callback = callback


class EasyPlaceholder:
    def __init__(
        self, identifier: str, callback: typing.Callable[[Player, list[str]], str]
    ):
        self.id = identifier
        self.callback = callback


### Main CommandManager class ###


class CommandManager:
    def __init__(self):
        self.commands = self.SlashCommandManager(self)
        self.executions = self.ExecutionManager(self)
        self.placeholders = self.PlaceholderManager(self)
        self._commands = []
        self._executions = []
        self._placeholders = []

    class SlashCommandManager:
        def __init__(self, command_manager):
            self.manager: CommandManager = command_manager

        def register(
            self,
            name: str,
            description: str,
            usages: list[str],
            permission: list[str] = "easyas.command.op",
            aliases: list[str] = [],
            functionality: list[SimpleFunctionality] = [],
        ):
            self.manager._commands.append(
                EasySlashCommand(
                    name, description, usages, permission, aliases, functionality
                )
            )

    class ExecutionManager:
        def __init__(self, command_manager):
            self.manager: CommandManager = command_manager

        def register(
            self, name: str, callback: typing.Callable[[Player, str, list[str]], None]
        ):
            self.manager._executions.append(EasyExecution(name, callback))

    class PlaceholderManager:
        def __init__(self, command_manager):
            self.manager: CommandManager = command_manager

        def register(
            self,
            identifier: str,
            callback: typing.Callable[[Player, list[str]], str],
        ):
            self.manager._placeholders.append(EasyPlaceholder(identifier, callback))
