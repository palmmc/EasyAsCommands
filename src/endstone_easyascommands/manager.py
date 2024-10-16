from endstone._internal.endstone_python import (
    Player,
)
import json
import os

from .form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    MessageFormData,
    MessageFormResponse,
)
from .Manage.add import add_command
from .Manage.edit import edit_command
from .Utils.utils import read_commands_config, write_commands_config, send_custom

from endstone.plugin import Plugin

### COMMAND MANAGER FUNCTIONALITY ###

commandData = read_commands_config()


def command_manager(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Command Manager")
    form.body("Click a command to edit it.")
    form.button("Add Command", "textures/ui/smithing-table-plus.png")
    form.button("Remove Command", "textures/ui/dark_minus.png")
    for command_name in commandData["commands"].keys():
        command = commandData["commands"][command_name]
        form.button(
            f"{command_name}\n{command['description']}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        if result.selection == 0:
            add_command(self, player, {"usages": [], "aliases": [], "permissions": []})
        elif result.selection == 1:
            remove_command(self, player)
        else:
            commands = commandData["commands"]
            cmdName = list(commands.keys())[result.selection - 2]
            command = commands[cmdName]
            edit_command(
                self,
                player,
                {
                    "name": cmdName,
                    "description": command["description"],
                    "usages": command["usages"],
                    "aliases": command["aliases"],
                    "permissions": command["permissions"],
                },
            )

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def remove_command(self: Plugin, player: Player):
    form = ActionFormData()
    form.title("Remove Command")
    form.body("Click a command to remove it.")
    for command_name in commandData["commands"].keys():
        command = commandData["commands"][command_name]
        form.button(
            f"{command_name}\n§7{command['description']}",
            "textures/ui/user_icon_white.png",
        )

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return
        commands = commandData["commands"]
        command = commands[list(commands.keys())[result.selection - 1]]
        confirm_remove_command(self, player, command)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def confirm_remove_command(self: Plugin, player: Player, command):
    form = MessageFormData()
    form.title("Confirm Removal")
    form.body(f"Are you sure you want to remove '{command['name']}'?")
    form.button1("Yes")
    form.button2("No")

    def remove_command(
        self: Plugin, player: Player, result: MessageFormResponse, command
    ):
        if result.canceled or result.selection == 2:
            return
        else:
            commandData["commands"].pop(command["name"])
            write_commands_config(commandData)
            send_custom(
                player,
                f"§cCommand §f'§6{command['name']}§f' §chas been removed.\n§eAttempting to reload server...",
            )

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: remove_command(
            self, player, response, command
        )
    )
