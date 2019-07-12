# Created by Lionel Kornberger at 2019-05-07
import sys
from configparser import ConfigParser
import os

DARWIN_CONFIG_FILE = '../config/darwin.ini'
WINDOWS_CONFIG_FILE = '../../config/windows.ini'
LINUX_CONFIG_FILE = '../../config/linux.ini'


def get_os_name():
    return sys.platform


def get_config_file():
    if get_os_name() == 'linux':
        return os.environ.get('CONFIG_FILE', LINUX_CONFIG_FILE)
    elif get_os_name() == 'win32':
        return os.environ.get('CONFIG_FILE', WINDOWS_CONFIG_FILE)
    else:
        return os.environ.get('CONFIG_FILE', DARWIN_CONFIG_FILE)


CONFIG_FILE = get_config_file()


def create_config():
    parser = ConfigParser()

    parser.read(CONFIG_FILE)
    return parser


CONFIG = create_config()


def get_config():
    return CONFIG
