***
# EasyAsCommands API
**EasyAsCommands** has its own API that developers can include in their plugins to integrate their plugin with EAC.

***
## Adding to Plugin
1) Download `eac_api.py` latest [release](../../../releases/).
2) Drop it into your plugin at the same level as your entry point script.
3) Add the following import to the top of your script:
   <br><br>
   ```python
   from .eac_api import CommandManager
   ```
4) Now set up your `CommandManager` class similarly to your plugin class.
   <br><br>
   ```python
   from .eac_api import CommandManager
   
   class EAC(CommandManager):
       def __init__(self):
           super().__init__()
       # Registry methods should be initialized.
   # Everything else can go wherever.
   ```
5) And you're done!
***
# Usage
The API includes many useful implementations, especially for registering types to integrate your plugin into EAC.

Here is a list of all available methods and attributes that can be used:
# `class` CommandManager
Parent class for command management.

#### `Example:`
```python
   from .eac_api import CommandManager
   
   class EAC(CommandManager):
       def __init__(self):
           super().__init__()
```

- ## `attr` commands
  > Contains methods for managing commands.
  - ### `def` register
    > #### `name: str`, `description: str`, `usages: list[str]`, `permissions?: list[str]`, `aliases?: list[str]`, `functionality?: list[{type: str, content: str}]`
    > 
    > Registers a slash command that can be managed by EasyAsCommands.
  ### `example.py`
  ```python
  ## Registering a Command ##
    class EAC(CommandManager):
        def __init__(self):
            super().__init__()

            self.commands.register(
                "jellydonut",
                "This is a test command.",
                ["/jellydonut <count: int>"],
                ["easyas.command.all"],
                ["jd"],
                [
                    {
                        "type": "donut_example",
                        "content": "{donut_count}!",
                    }
                ],
            )
  ```

- ## `attr` executions
  > Contains methods for managing executions.
  - ### `def` register
    > #### `name: str`, `callback: Callable[[Player, str, list[str]], None]`
    > 
    > Registers an execution type for use in commands.
  ### `example.py`
  ```python
  ## Registering an Execution Type ##
    class EAC(CommandManager):
        def __init__(self):
            super().__init__()

            self.executions.register("donut_example", example_execution)

    def example_execution(player: Player, content: str, args):
        player.send_message(f"§9How many donuts? §c{content}")
  ```

- ## `attr` placeholders
  > Contains methods for managing placeholders.
  - ### `def` register
    > #### `identifier: str`, `callback: Callable[[Player, list[str]], str]`
    > 
    > Registers a placeholder for use in commands.

  ### `example.py`
  ```python
  ## Registering a Placeholder ##
    class EAC(CommandManager):
        def __init__(self):
            super().__init__()

            self.placeholders.register("donut_count", example_placeholder)


    def example_placeholder(player: Player, args):
        if len(args) == 0:
            return "0 donuts"
        else:
            return f"{args[0]} donuts"

  ```
***
`?` = Optional
