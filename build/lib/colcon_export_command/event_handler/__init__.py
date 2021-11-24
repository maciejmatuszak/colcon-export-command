"""Environment variable to override the default executor"""
from colcon_core.environment_variable import EnvironmentVariable

COLCON_COMMAND_EXPORT_PATH_ENVIRONMENT_VARIABLE = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_PATH',
        'Overrides export path for "colcon-export-command" plugin')
