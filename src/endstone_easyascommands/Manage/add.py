from .submit import submit_command

from endstone.plugin import Plugin
from ..form_wrapper import (
    ActionFormData,
    ActionFormResponse,
    MessageFormData,
    MessageFormResponse,
)
from endstone._internal.endstone_python import Player

from ..Manage.edit import (
    manage_aliases,
    manage_permissions,
    manage_usages,
    set_command_description,
    set_command_name,
)


def add_command(self: Plugin, player: Player, command):
    form = ActionFormData()
    form.title("Add Command")
    form.button("Set Name")
    form.button("Set Description")
    form.button("Manage Usages")
    form.button("Manage Aliases")
    form.button("Manage Permissions")
    form.button("Submit")

    def submit(self: Plugin, player: Player, result: ActionFormResponse):
        if result.canceled:
            return confirm_exit_add_command(self, player, command)
        if result.selection == 0:
            set_command_name(self, player, command)
        elif result.selection == 1:
            set_command_description(self, player, command)
        elif result.selection == 2:
            manage_usages(self, player, command)
        elif result.selection == 3:
            manage_aliases(self, player, command)
        elif result.selection == 4:
            manage_permissions(self, player, command)
        elif result.selection == 5:
            submit_command(self, player, command)

    form.show(player).then(
        lambda player=Player, response=ActionFormResponse: submit(
            self, player, response
        )
    )


def confirm_exit_add_command(self: Plugin, player: Player, command):
    form = MessageFormData()
    form.title("Confirm Exit")
    form.body("Are you sure you want to exit without saving?")
    form.button1("Submit")
    form.button2("Cancel")

    def exit_add_command(
        self: Plugin, player: Player, result: MessageFormResponse, command
    ):
        if result.canceled or result.selection == 0:
            return
        else:
            add_command(self, player, command)

    form.show(player).then(
        lambda player=Player, response=MessageFormResponse: exit_add_command(
            self, player, response, command
        )
    )
