# Copyright 2021 Maciej Matuszak
# Licensed under the Apache License, Version 2.0
import os
from datetime import datetime
from pathlib import Path

from colcon_core.event.command import Command
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.executor import Job
from colcon_core.location import get_log_path, create_log_path
from colcon_core.plugin_system import satisfies_version
import json


def deduceCmakeCommandType(command: Command, job: Job) -> str:
    assert isinstance(job, Job)
    # detect type of cmake command
    cmakeCommand = "configure"
    if '--build' in command.cmd:
        cmakeCommand = "build"
    elif '--install' in command.cmd:
        cmakeCommand = 'install'
    return cmakeCommand


class JsonCommandExporter(EventHandlerExtensionPoint):
    """
    Exports cmake commands as json to log dir
    """

    # this handler is disabled by default
    ENABLED_BY_DEFAULT = False

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(EventHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        self.enabled = JsonCommandExporter.ENABLED_BY_DEFAULT

    def __call__(self, event):  # noqa: D102
        command = event[0]

        # we are interested only in Command
        if not type(command) == Command:
            return

        job: Job = event[1]

        # full file path
        filePath = self.getFileName(job, command)

        # convert Command to dictionary for json dump
        jDict = {slot: getattr(command, slot) for slot in command.__slots__}

        with open(filePath, 'w') as f:
            json.dump(jDict, f, indent=4)

    def getFileName(self, job: Job, command: Command) -> Path:

        if job.task.PACKAGE_TYPE == 'cmake':
            filePart: str = deduceCmakeCommandType(command, job)
        else:
            filePart: str = datetime.now().strftime("%Y_%m_%d-%H:%M:%S.%f")

        envPath = os.getenv('CMAKE_COMMAND_EXPORT_PATH')

        if envPath is not None:
            path = Path(envPath.strip(' '))
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
