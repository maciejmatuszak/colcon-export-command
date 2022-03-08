# Copyright 2021-2022 Maciej Matuszak
# Licensed under the Apache License, Version 2.0
import os
import re
from datetime import datetime
from pathlib import Path
import json
from typing import Optional

from colcon_core.event.command import Command
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.executor import Job
from colcon_core.location import get_log_path, create_log_path
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from colcon_export_command.event_handler import COLCON_COMMAND_EXPORT_PATH_ENVIRONMENT_VARIABLE, \
    COLCON_COMMAND_EXPORT_JETBRAIN_ENVIRONMENT_VARIABLE, COLCON_COMMAND_EXPORT_JETBRAIN_ENV_VARS_ENVIRONMENT_VARIABLE
from colcon_export_command.xml.models import Project, Configuration, AdditionalGenerationEnvironment, Envs, Env, \
    Component, Configurations

logger = colcon_logger.getChild(__name__)


def deduceCmakeCommandType(command: Command) -> str:
    """
    based on @command content it will try to deduce the type of cmake call
    @param command:
    @return: one of the following strings 'configure', 'build',  'install'
    """

    cmakeCommand = 'configure'
    if '--build' in command.cmd:
        cmakeCommand = 'build'
    elif '--install' in command.cmd:
        cmakeCommand = 'install'
    return cmakeCommand


def isCmdOption(item: str) -> bool:
    if item.startswith('-'):
        return True
    return False


def isExistingDir(item) -> bool:
    if os.path.exists(item) and os.path.isdir(item):
        return True
    return False


def isExistingFile(item) -> bool:
    if os.path.exists(item) and os.path.isfile(item):
        return True
    return False


class JsonCommandExporter(EventHandlerExtensionPoint):
    """
    Exports cmake commands as json to log dir
    """

    # this handler is disabled by default
    ENABLED_BY_DEFAULT = False

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(EventHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        self.ignoreEnvVariables = ['_', 'SHELL', 'PWD']

        self.exportPath: Optional[str] = os.getenv(COLCON_COMMAND_EXPORT_PATH_ENVIRONMENT_VARIABLE.name)
        self.jetBrainExport: bool = bool(os.getenv(COLCON_COMMAND_EXPORT_JETBRAIN_ENVIRONMENT_VARIABLE.name))

        # setup selective export variables if available
        temp = os.getenv(COLCON_COMMAND_EXPORT_JETBRAIN_ENV_VARS_ENVIRONMENT_VARIABLE.name, None)
        if temp:
            self.jetBrainExportVariables = re.split(':|;|,| ', temp)
            self.jetBrainExportVariables = [it for it in self.jetBrainExportVariables if it]
            self.jetBrainExport = True
        else:
            self.jetBrainExportVariables = None

        if self.exportPath is not None or self.jetBrainExport or self.jetBrainExportVariables:
            self.enabled = True
        else:
            self.enabled = JsonCommandExporter.ENABLED_BY_DEFAULT

    def __call__(self, event):  # noqa: D102
        command: Command = event[0]

        # we are interested only in Command
        if not type(command) == Command:
            return

        job: Job = event[1]

        self.exportJsonCommand(command, job)

        self.exportClionCmakeSettings(command)

    def exportClionCmakeSettings(self, command):
        if not self.jetBrainExport:
            return

        cmakeVerb = deduceCmakeCommandType(command)
        if cmakeVerb == 'configure':

            configOpptions = []
            srcDir = None
            # parse the command elements
            for item in command.cmd:
                # cmake commandline
                if item == 'cmake':
                    continue
                # cmake commandline - full path
                if str(item).endswith('cmake') and isExistingFile(item):
                    continue
                # usually second item in command is source dir
                if not isCmdOption(item) and isExistingDir(item):
                    srcDir = item
                    continue
                configOpptions.append(item)
            srcDirPath = Path(srcDir)
            ideaPath = srcDirPath / '.idea'
            if ideaPath.exists():
                cmakeXmlPath = ideaPath / 'cmake.xml'

                profileEnabled = True
                configName = 'RelWithDebInfo'
                toolChainName = 'Default'
                passSystemEnv = False
                buildOptions = ''

                if cmakeXmlPath.exists():
                    # load and update
                    parser = XmlParser(context=XmlContext())
                    projectToSave = parser.parse(str(cmakeXmlPath), Project)

                    temp = [cfg for cfg in projectToSave.component.configurations.configuration
                            if cfg.profile_name == 'colcon']
                    if temp:
                        oldConfig = temp[0]
                        configName = oldConfig.config_name
                        toolChainName = oldConfig.toolchain_name
                        profileEnabled = oldConfig.enabled
                        passSystemEnv = oldConfig.generation_pass_system_environment
                        buildOptions = oldConfig.build_options

                    # remove existing
                    projectToSave.component.configurations.configuration = [
                        cfg for cfg in
                        projectToSave.component.configurations.configuration
                        if cfg.profile_name != 'colcon']

                else:
                    projectToSave = Project(version=4,
                                            component=Component(name='CMakeSharedSettings',
                                                                configurations=Configurations()))

                envs = Envs()
                for envKey, envVal in command.env.items():
                    if envKey in self.ignoreEnvVariables:
                        continue
                    if self.jetBrainExportVariables:
                        if envKey in self.jetBrainExportVariables:
                            envs.env.append(Env(name=envKey, value=envVal))
                    else:
                        envs.env.append(Env(name=envKey, value=envVal))

                config = Configuration(profile_name='colcon',
                                       enabled=profileEnabled,
                                       generation_dir=command.cwd,
                                       config_name=configName,
                                       toolchain_name=toolChainName,
                                       generation_options=' '.join(configOpptions),
                                       generation_pass_system_environment=passSystemEnv,
                                       build_options=buildOptions,
                                       additional_generation_environment=AdditionalGenerationEnvironment(
                                               envs))
                projectToSave.component.configurations.configuration.append(config)

                serializerCfg = SerializerConfig(pretty_print=True)
                serializer = XmlSerializer(config=serializerCfg)
                with open(cmakeXmlPath, 'w') as fd:
                    serializer.write(fd, projectToSave)
                    pass

            print(f'Configure for {command.cmd[1]}')
            logger.info(f'Configure for {command.cmd[1]}')

    def exportJsonCommand(self, command, job):
        # full file path
        filePath = self.getExportFileName(job, command)
        # convert Command to dictionary for json dump
        jDict = {slot: getattr(command, slot) for slot in command.__slots__}
        with open(filePath, 'w') as f:
            json.dump(jDict, f, indent=4)

    def getExportFileName(self, job: Job, command: Command) -> Path:

        if job.task.PACKAGE_TYPE in ('cmake', 'ros.catkin'):
            filePart: str = deduceCmakeCommandType(command)
        else:
            filePart: str = datetime.now().strftime("%Y_%m_%d-%H:%M:%S.%f")

        if self.exportPath is not None:
            path = Path(self.exportPath.strip(' '))
            os.makedirs(str(path), exist_ok=True)
            path /= f'{job.identifier}_command_{filePart}.json'

        else:
            # make sure base log path exists
            create_log_path(self.context.args.verb_name)

            # lets put the files in per project dir
            path = get_log_path() / job.identifier
            os.makedirs(str(path), exist_ok=True)

            path = path / f'command_{filePart}.json'

        return path
