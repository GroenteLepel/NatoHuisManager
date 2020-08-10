import inspect
import sys
import os

# Add the src directory to our python path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))


from natohuismanager.commands import all_command_handlers


def get_methods(object):
    return [method_name for method_name in dir(object) if callable(getattr(object, method_name))]

commands = {}

object_methods = get_methods(object)
for handler in all_command_handlers:
    # Filter out default methods like __init__
    for m in get_methods(handler):
        if m not in object_methods:
            description = inspect.getdoc(getattr(handler, m))
            if description:
                commands[m] = description.split('\n')[0]


for command, description in commands.items():
    print(f"{command} - {description}")