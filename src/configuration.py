from dataclasses import dataclass

import dataconf


class ConfigurationBase:

    @staticmethod
    def fromDict(parameters: dict):
        return dataconf.dict(parameters, Configuration, ignore_unexpected=True)


@dataclass
class Configuration(ConfigurationBase):
    report_types: list[str]
    on_behalf_of_content_owner: bool = False
    content_owner_id: str = ''
    debug: bool = False
