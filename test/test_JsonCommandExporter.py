import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from unittest import TestCase, mock
from colcon_core.event.command import Command
from colcon_core.executor import Job

from colcon_export_command.event_handler import EV_COLCON_COMMAND_EXPORT_PATH, \
    EV_COLCON_COMMAND_EXPORT_CLION
from colcon_export_command.event_handler.JsonCommandExporter import JsonCommandExporter

testCommandFile = Path(__file__).parent / 'command_configure.json'


class FakeTask:
    def __init__(self):
        self.PACKAGE_TYPE = 'cmake'


class TestJsonCommandExporter(TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.testProjectName = 'projName'
        self.testCommand: Optional[Command] = None
        self.testJob: Optional[Job] = None
        self.testObject: Optional[JsonCommandExporter] = None
        self.tempDir: Optional[TemporaryDirectory] = None
        self.testSourceDir: Optional[Path] = None

    def setUp(self) -> None:
        super().setUp()

        self.tempDir = TemporaryDirectory()

        self.envPatcher = mock.patch.dict(os.environ, {
            EV_COLCON_COMMAND_EXPORT_PATH.name: self.tempDir.name,
            EV_COLCON_COMMAND_EXPORT_CLION.name: 'True'})
        self.envPatcher.start()
        self.tempDirPath = Path(self.tempDir.name)
        self.testSourceDir = self.tempDirPath / 'src'
        self.testSourceDir.joinpath('.idea').mkdir(exist_ok=True, parents=True)
        self.testCommand = Command(
                cmd=[
                    'cmake',
                    str(self.testSourceDir),
                    '-DCMAKE_BUILD_TYPE=Debug',
                    '-DCMAKE_CXX_STANDARD=17',
                    '-DCMAKE_CXX_STANDARD_REQUIRED=YES',
                    '-DCMAKE_DEBUG_POSTFIX=d'],
                cwd=str(self.testSourceDir),
                env={
                    'COLCON_HOME': './.colcon'
                },
                shell=False
        )

        self.testJob = Job(
                identifier=self.testProjectName,
                dependencies=[],
                task=FakeTask(),
                task_context=None)
        self.testObject = JsonCommandExporter()

    def tearDown(self) -> None:
        super().tearDown()
        self.tempDir.cleanup()
        self.envPatcher.stop()

    def readCommand(self, filePath: Path) -> Command:
        with open(filePath, mode='r') as fd:
            dd = json.load(fd)
            return Command(**dd)
        raise Exception(f'Failed to read "{filePath}"')

    def test_json_command_exporter(self):
        self.testObject([self.testCommand, self.testJob])
        resFile = self.tempDirPath / f'{self.testProjectName}_command_configure.json'
        resCmd = self.readCommand(resFile)
        self.assertFalse(resCmd.shell)
