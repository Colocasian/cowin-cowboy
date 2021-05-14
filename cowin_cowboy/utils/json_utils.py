# json_utils.py -- utilities related to JSONs
# Copyright (C) 2021  Rishvic Pushpakaran

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["read_json_file"]

from os.path import isfile
from json import load, JSONDecodeError
from logging import getLogger

_logger = getLogger(__name__)


def read_json_file(json_file):
    """Reads the config file, and returns the object
    :param json_file: location of config file
    :type json_file: os.PathLike
    :return: Decoded config file, as a dictionary
    :rtype: dict
    """
    if isfile(json_file):
        try:
            with open(json_file) as conf_fp:
                data = load(conf_fp)
                return data
        except JSONDecodeError:
            _logger.error("Could not decode config file '{}'".format(json_file))
        except IOError:
            _logger.error("Could not open file '{}'".format(json_file))
    else:
        _logger.error("No file found at '{}'".format(json_file))

    return None
