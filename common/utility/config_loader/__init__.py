from pydantic.dataclasses import dataclass

from common.utility.config_loader.read_json import JsonConfigReader
from common.utility.config_loader.read_yaml import YamlConfigReader


@dataclass
class ConfigReaderInstance:
    json = JsonConfigReader()
    yaml = YamlConfigReader()
