import collections
import configparser
import pathlib
from typing import Any


# Support parsing duplicated options in inf
# https://stackoverflow.com/a/15848928/1592410
class KeyCaseInsensitiveValueExtendedDict(collections.OrderedDict):
    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, list) and key in self:
            self[key].extend(value)
            return
        super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        k: str
        for k in self.keys():
            if k.lower() != key.lower():
                continue
            return super().__contains__(k)
        return False

    def __getitem__(self, key: str) -> Any:
        k: str
        for k in self.keys():
            if k.lower() != key.lower():
                continue
            return super().__getitem__(k)


def parse_inf(inf_path: pathlib.Path) -> configparser.ConfigParser:
    config: configparser.ConfigParser = configparser.ConfigParser(
        allow_no_value=True, dict_type=KeyCaseInsensitiveValueExtendedDict, strict=False)
    config.optionxform = str
    config.read(inf_path, encoding='utf-16')
    return config


def get_cat(inf_path: pathlib.Path) -> pathlib.Path:
    inf_content: configparser.ConfigParser = parse_inf(inf_path)
    return inf_path.parent / inf_content['Version'].get('CatalogFile')


def get_bundled_files(inf_path: pathlib.Path) -> set[pathlib.Path]:
    res: set[pathlib.Path] = set()
    inf_content: configparser.ConfigParser = parse_inf(inf_path)

    if 'SourceDisksFiles' not in inf_content:
        return res

    key: str
    for key in inf_content['SourceDisksFiles']:
        src_file: str = key
        res.add(inf_path.parent / src_file)

    return res


def get_version(self) -> str:
    inf_content: configparser.ConfigParser = parse_inf(list(self.driver_dir.rglob('*.inf'))[-1])
    return '.'.join(inf_content['Version'].get('DriverVer').split(',')[1:]).strip()
