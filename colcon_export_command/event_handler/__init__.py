"""Environment variable to override the default executor"""
from colcon_core.environment_variable import EnvironmentVariable

EV_COLCON_COMMAND_EXPORT_PATH = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_PATH',
        'Overrides export path for "colcon-export-command" plugin')

EV_COLCON_COMMAND_EXPORT_CLION = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION',
        'Export cmake configure command to project .idea/cmake.xml')

EV_COLCON_COMMAND_EXPORT_CLION_PROFILE_ENABLED = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_PROFILE_ENABLED',
        'enable the exported profile. [default: True]')

EV_COLCON_COMMAND_EXPORT_CLION_PROFILE_NAME = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_PROFILE_NAME',
        'name of the exported profile. [default: "colcon_{CMAKE_BUILD_TYPE}"]')

EV_COLCON_COMMAND_EXPORT_CLION_ENV_VARS = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_ENV_VARS',
        'separated list of environment variables (case sensitive) to preserve in env. '
        'Separator can be: ",", ";", ":", " "')

EV_COLCON_COMMAND_EXPORT_CLION_BUILD_OPTIONS = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_BUILD_OPTIONS',
        'default cmake build options i.e. [default: "-- -j 9"]')

EV_COLCON_COMMAND_EXPORT_CLION_TOOLCHAIN = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_TOOLCHAIN',
        'clion toolchain to use if not set [default: "Default"]')

EV_COLCON_COMMAND_EXPORT_CLION_BUILD_TYPE = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_BUILD_TYPE',
        'cmake build type to use when not set. [default:"RelWithDebInfo"]')

EV_COLCON_COMMAND_EXPORT_CLION_PASS_SHELL_ENV = EnvironmentVariable(
        'COLCON_COMMAND_EXPORT_CLION_PASS_SHELL_ENV',
        'pass shell environment flag to use when not set. [default: False]')

