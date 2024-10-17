from endstone._internal.endstone_python import Player


class ExecutionTypes:
    executions = []

    @staticmethod
    def get_types():
        types = []
        for execution in ExecutionTypes.executions:
            types.append(execution.name)
        return types

    @staticmethod
    def get_execution(
        name,
    ):
        for execution in ExecutionTypes.executions:
            if execution.name == name:
                return execution.callback
        return None


class PlaceholderTypes:
    placeholders = []

    @staticmethod
    def get_types():
        types = []
        for placeholder in PlaceholderTypes.placeholders:
            types.append(placeholder.id)
        return types

    @staticmethod
    def get_placeholder(
        id,
    ):
        for placeholder in PlaceholderTypes.placeholders:
            if placeholder.id == id:
                return placeholder.callback
        return None


class ConditionTypes:
    conditions = []

    @staticmethod
    def get_types():
        types = []
        for condition in ConditionTypes.conditions:
            types.append(condition.name)
        return types

    @staticmethod
    def get_condition(
        name,
    ):
        for condition in ConditionTypes.conditions:
            if condition.name == name:
                return condition.callback
        return None
