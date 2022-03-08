from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Env:
    class Meta:
        name = "env"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Envs:
    class Meta:
        name = "envs"

    env: List[Env] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class AdditionalGenerationEnvironment:
    class Meta:
        name = "ADDITIONAL_GENERATION_ENVIRONMENT"

    envs: Optional[Envs] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Configuration:
    class Meta:
        name = "configuration"

    profile_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "PROFILE_NAME",
            "type": "Attribute",
        }
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ENABLED",
            "type": "Attribute",
        }
    )
    generation_dir: Optional[str] = field(
        default=None,
        metadata={
            "name": "GENERATION_DIR",
            "type": "Attribute",
        }
    )
    config_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "CONFIG_NAME",
            "type": "Attribute",
        }
    )
    toolchain_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "TOOLCHAIN_NAME",
            "type": "Attribute",
        }
    )
    generation_options: Optional[str] = field(
        default=None,
        metadata={
            "name": "GENERATION_OPTIONS",
            "type": "Attribute",
        }
    )
    generation_pass_system_environment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "GENERATION_PASS_SYSTEM_ENVIRONMENT",
            "type": "Attribute",
        }
    )
    build_options: Optional[str] = field(
        default=None,
        metadata={
            "name": "BUILD_OPTIONS",
            "type": "Attribute",
        }
    )
    additional_generation_environment: Optional[AdditionalGenerationEnvironment] = field(
        default=None,
        metadata={
            "name": "ADDITIONAL_GENERATION_ENVIRONMENT",
            "type": "Element",
        }
    )


@dataclass
class Configurations:
    class Meta:
        name = "configurations"

    configuration: List[Configuration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Component:
    class Meta:
        name = "component"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    configurations: Optional[Configurations] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Project:
    class Meta:
        name = "project"

    version: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    component: Optional[Component] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
