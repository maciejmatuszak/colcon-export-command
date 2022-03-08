"""Environment variable to override the default executor"""
from colcon_core.environment_variable import EnvironmentVariable

COLCON_COMMAND_EXPORT_PATH_ENVIRONMENT_VARIABLE = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_PATH',
        'Overrides export path for "colcon-export-command" plugin')

COLCON_COMMAND_EXPORT_JETBRAIN_ENVIRONMENT_VARIABLE = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_JETBRAIN',
        'Export cmake configure command to project .idea/cmake.xml')

COLCON_COMMAND_EXPORT_JETBRAIN_ENV_VARS_ENVIRONMENT_VARIABLE = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_JETBRAIN_ENV_VARS',
        'separated list of environment variables (case sensitive) to preserve in env. '
        'Separator can be: ",", ";", ":", " "')
