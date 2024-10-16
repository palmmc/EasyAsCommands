from endstone._internal.endstone_python import Player
from endstone.plugin import Plugin
from ..Utils.utils import (
    read_commands_config,
    write_commands_config,
    send_custom,
    error_custom,
)


def submit_command(self: Plugin, player: Player, command):
    if "name" not in command:
        error_custom(player, "Incomplete command: Property '§4name§c' is missing.")
        return
    if "description" not in command:
        error_custom(
            player, "Incomplete command: Property '§4description§c' is missing."
        )
        return
    if "usages" not in command:
        error_custom(player, "Incomplete command: Property '§4usages§c' is missing.")
        return
    if "aliases" not in command:
        error_custom(player, "Incomplete command: Property '§4aliases§c' is missing.")
        return
    if "permissions" not in command:
        error_custom(
            player, "Incomplete command: Property '§4permissions§c' is missing."
        )
        return
    commandData = read_commands_config()
    commandData["commands"][command["name"]] = {
        "description": command["description"],
        "usages": command["usages"],
        "aliases": command["aliases"],
        "permissions": command["permissions"],
    }
    write_commands_config(commandData)
    send_custom(
        player,
        f"§aCommand §f'§6{command['name']}§f' §ahas been saved.\n§eServer has been reloaded successfully!",
    )
    try:
        self.server.reload()
    except Exception as e:
        error_custom(player, f"Failed to reload server: {e}")
        return
