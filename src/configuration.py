from dataclasses import dataclass
import dataconf
from enum import Enum


class InputVariantEnum(Enum):
    use_login_owner = "use_login_owner"
    use_selected_owner = "use_selected_owner"


class ConfigurationBase:

    @staticmethod
    def fromDict(parameters: dict):
        return dataconf.dict(parameters, Configuration, ignore_unexpected=True)


@dataclass
class Configuration(ConfigurationBase):
    input_variant: InputVariantEnum
    report_types: list[str]
    history_days: int = 0
    content_owner: str = ''
    debug: bool = False


if __name__ == '__main__':
    _parameters = {
        "#api_token": "fdsfda",
        "history_days": 3,
        "input_variant": "use_selected_owner",
        "content_owner": "1434234",
        "report_types": ["channel_cards_a1", "channel_device_os_a2"],
        "debug": False
    }
    conf = Configuration.fromDict(_parameters)
    pass
