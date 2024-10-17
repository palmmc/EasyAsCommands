import typing

import json
from .manager import command_manager
from .Utils.utils import read_commands_config, error_custom, reset_commands, send_custom
from endstone._internal.endstone_python import (
    ColorFormat,
    Player,
)
from endstone.command import Command, CommandSender
from endstone.event import event_handler
from endstone.plugin import Plugin
from .API.integrations import APIHandler
from .API.types import ExecutionTypes, PlaceholderTypes
import re


class EasyAsCommands(Plugin):
    prefix = "EasyAsCommands"
    api_version = "0.5"
    load = "POSTWORLD"

    # Read command data.
    commandData = read_commands_config()
    # Add mandatory commands.
    commandData["commands"]["commands"] = {
        "description": "Opens command manager.",
        "usages": ["/commands"],
        "aliases": ["cmds", "cmdmanager", "commandmanager"],
        "permissions": ["easyas.command.manager"],
    }
    commandData["commands"]["resetcommands"] = {
        "description": "Resets all EAC commands.",
        "usages": ["/resetcommands"],
        "aliases": ["resetcmds"],
        "permissions": ["easyas.command.reset"],
    }
    commands = commandData["commands"]

    permissions = {
        "easyas.command.manager": {
            "description": "Command manager permission.",
            "default": "op",
        },
        "easyas.command.reset": {
            "description": "Reset commands permission.",
            "default": "op",
        },
        "easyas.command.all": {
            "description": "All players can use this.",
            "default": True,
        },
        "easyas.command.op": {
            "description": "Only operators can use this.",
            "default": "op",
        },
    }

    def on_enable(self) -> None:
        self.register_events(self)

    def on_load(self):
        self.logger.info(
            f"""
        {ColorFormat.BLUE}                                                     
      _____             _____     _____                           _     
     |   __|___ ___ _ _|  _  |___|     |___ _____ _____ ___ ___ _| |___ 
     |   __| .'|_ -| | |     |_ -|   --| . |     |     | .'|   | . |_ -|
     |_____|__,|___|_  |__|__|___|_____|___|_|_|_|_|_|_|__,|_|_|___|___|   by palm1
                   |___|      
                                                            
        {ColorFormat.RESET}"""
        )
        self.logger.info(
            f"\n> {ColorFormat.DARK_BLUE}{ColorFormat.BOLD}Welcome to EasyAsCommands!{ColorFormat.RESET}\n> {ColorFormat.YELLOW}API Version: {self.api_version}{ColorFormat.RESET}\n> {ColorFormat.LIGHT_PURPLE}For help and updates, visit [ {ColorFormat.BLUE}https://github.com/palmmc/EasyAsCommands {ColorFormat.LIGHT_PURPLE}]{ColorFormat.RESET}"
        )
        # Begin task.
        APIHandler.discover_integrations(self)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]):
        # You can also handle commands here instead of setting an executor in on_enable if you prefer
        server = self.server
        if not (isinstance(sender, Player)):
            server.logger.info("Only players can use this command.")
            return
        player = sender
        if command.name == "commands":
            command_manager(self, player)
            return
        elif command.name == "resetcommands":
            reset_commands(self, player)
            return
        if command.name not in self.commandData["functions"]:
            send_custom(
                player,
                "§8This command doesn't have any functionality yet.\n§9Add it in the command manager!",
            )
            return
        function = self.commandData["functions"][command.name]
        for func in function:
            line = func["content"]
            try:
                # Score Placeholders
                line = self.replace_score_placeholders(line)
                # Player Placeholder
                if "{player}" in line:
                    line = line.replace("{player}", player.name)
                i = 0
                # Argument Placeholders
                for arg in args:
                    if ("{" + str(i) + "}") in line:
                        line = line.replace("{" + str(i) + "}", arg)
                    i += 1
                # Custom Placeholders
                for placeholder in PlaceholderTypes.get_types():
                    if "{" + placeholder + "}" in line:
                        line = line.replace(
                            "{" + placeholder + "}",
                            PlaceholderTypes.get_placeholder(placeholder)(player, args),
                        )

                if func["type"] == "command":
                    server.dispatch_command(server.command_sender, line)
                else:
                    ExecutionTypes.get_execution(func["type"])(player, line, args)
            except Exception as e:
                server.logger.error(f"Error: {e}")
                error_custom(
                    player,
                    f"An error occurred while executing the command.\n§4Please report this to an admin.",
                )

    def replace_score_placeholders(player: Player, string: str):
        server = player.server
        placeholders = re.findall(r"\{(.*?)\}", string)
        for placeholder in placeholders:
            if placeholder.startswith("score:"):
                objective = placeholder.split(":", 1)[1]
                value = (
                    server.scoreboard.get_objective(objective).get_score(player).value
                )
                string = re.sub(
                    r"\{" + re.escape(placeholder) + r"\}", str(value), string
                )

        return string
