import pathlib
from dataclasses import asdict, dataclass, field
from typing import Optional, Union

import yaml

from lightning_app.utilities.name_generator import get_unique_name

_APP_CONFIG_FILENAME = ".lightning"


@dataclass
class AppConfig:
    """The AppConfig holds configuration metadata for the application.

    Args:
        name: Optional name of the application. If not provided, auto-generates a new name.
    """

    name: str = field(default_factory=get_unique_name)
    cluster_id: Optional[str] = field(default=None)

    def save_to_file(self, path: Union[str, pathlib.Path]) -> None:
        """Save the configuration to the given file in YAML format."""
        path = pathlib.Path(path)
        with open(path, "w") as file:
            yaml.dump(asdict(self), file)

    def save_to_dir(self, directory: Union[str, pathlib.Path]) -> None:
        """Save the configuration to a file '.lightning' to the given folder in YAML format."""
        self.save_to_file(_get_config_file(directory))

    @classmethod
    def load_from_file(cls, path: Union[str, pathlib.Path]) -> "AppConfig":
        """Load the configuration from the given file."""
        with open(path) as file:
            config = yaml.safe_load(file)
        return cls(**config)

    @classmethod
    def load_from_dir(cls, directory: Union[str, pathlib.Path]) -> "AppConfig":
        """Load the configuration from the given folder.

        Args:
            directory: Path to a folder which contains the '.lightning' config file to load.
        """
        return cls.load_from_file(pathlib.Path(directory, _APP_CONFIG_FILENAME))


def _get_config_file(source_path: Union[str, pathlib.Path]) -> pathlib.Path:
    """Get the Lightning app config file '.lightning' at the given source path.

    Args:
        source_path: A path to a folder or a file.
    """
    source_path = pathlib.Path(source_path).absolute()
    if source_path.is_file():
        source_path = source_path.parent

    return pathlib.Path(source_path / _APP_CONFIG_FILENAME)
