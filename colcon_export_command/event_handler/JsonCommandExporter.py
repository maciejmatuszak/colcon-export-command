# Copyright 2021 Maciej Matuszak
# Licensed under the Apache License, Version 2.0
import os
from datetime import datetime

from colcon_core.event.command import Command
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.executor import Job
from colcon_core.location import get_log_path, create_log_path
from colcon_core.plugin_system import satisfies_version
import json


def createCmakeFileName(command: Command, job: Job) -> str:
    assert isinstance(job, Job)
    # detect type of cmake command
    cmakeCommand = "configure"
    if '--build' in command.cmd:
        cmakeCommand = "build"
    elif '--install' in command.cmd:
        cmakeCommand = 'install'
    fileName = f'cmake_{cmakeCommand}.json'
    return fileName


class JsonCommandExporter(EventHandlerExtensionPoint):
    """
    Exports cmake commands: :py:class:`colcon_core.event.command.Command` as json to log dir
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

        # workout export file name
        if job.task.PACKAGE_TYPE == 'cmake':
            fileName = createCmakeFileName(command, job)
        else:
            fileName = datetime.now().strftime("command_%Y_%m_%d-%H:%M:%S.%f.json")

        # full file path
        filePath = self.getProjectLogFilePath(job) / fileName

        # convert Command to dictionary for json dump
        jDict = {slot: getattr(command, slot) for slot in command.__slots__}

        with open(filePath, 'w') as f:
            json.dump(jDict, f, indent=4)

    def getProjectLogFilePath(self, job):
        # make sure base log path exists
        create_log_path(self.context.args.verb_name)

        # lets put the files in per project dir
        base_path = get_log_path() / job.identifier
        os.makedirs(str(base_path), exist_ok=True)

        return base_path
