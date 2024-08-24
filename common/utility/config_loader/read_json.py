import json
from abc import ABC
from pathlib import Path

from common.config import settings
from common.utility.config_loader.config_interface import ConfigReaderInterface
from common.utility.config_loader.serializer import Struct


class JsonConfigReader(ConfigReaderInterface, ABC):

    def __init__(self):
        super(JsonConfigReader, self).__init__()

    def read_config_from_file(self, config_filename: str, return_dict: bool = False):
        conf_path = Path(__file__).joinpath(settings.APP_CONFIG.SETTINGS_DIR, config_filename)
        with open(conf_path) as file:
            config = json.load(file)
        config_object = Struct(**config) if not return_dict else config
        return config_object
