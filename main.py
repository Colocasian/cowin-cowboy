# main.py -- main user interface for cowin-cowboy
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

from argparse import ArgumentParser
from datetime import date, timedelta
from json import dumps, load, JSONDecodeError
import logging
from os import path
import sys
from os.path import isfile

from appdirs import user_config_dir
from cowin_cowboy.pub_checker import check_available_slots
from cowin_cowboy.filters import filter_available_centers
from cowin_cowboy.utils.api_utils import merge_center_dicts

logger = logging.getLogger(__name__)


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
            logger.error("Could not decode config file '{}'".format(json_file))
        except IOError:
            logger.error("Could not open file '{}'".format(json_file))
    else:
        logger.error("No file found at '{}'".format(json_file))

    return None


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="cowin-cowboy",
        description="Checks for available vaccination slots via Co-WIN API",
    )
    parser.add_argument(
        "-l",
        "--log",
        default=logging.getLevelName(logging.ERROR),
        help="set logging verbosity (defaults to ERROR)",
    )
    parser.add_argument("-c", "--config", help="path to custom config file")

    args = parser.parse_args()

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        logging.basicConfig(level=logging.ERROR)
        logger.error("Invalid log value '{}'".format(args.log))
        sys.exit(1)
    logging.basicConfig(level=numeric_level)

    conf_file = args.config
    if conf_file is None:
        conf_dir = user_config_dir("cowin-cowboy", "Colocasian")
        conf_file = path.join(conf_dir, "config.json")
    logger.info("Parsing config file '{}'...".format(conf_file))
    config = read_json_file(conf_file)

    if config is not None:
        available_centers = {}

        if "locations" in config:
            locations = config["locations"]
            weeks_to_check = max(1, config.get("weeks", 1))
            date_today = date.today()

            logger.info("Checking API for available centers...")
            for i in range(0, weeks_to_check):
                slots_this_week = check_available_slots(
                    date_today + timedelta(weeks=i), locations
                )
                merge_center_dicts(available_centers, slots_this_week)
        else:
            logger.error('"locations" key not found in config')
            sys.exit(1)

        if "filters" in config:
            filters = config.get("filters")
            logger.info("Filtering centers according to info")
            available_centers = filter_available_centers(available_centers, filters)
        else:
            logger.warning('No "filters" field found in config')

        print(dumps(available_centers, sort_keys=True, indent=2))
        logger.info("{} centers are available".format(len(available_centers)))
    else:
        logger.error(
            "Error while trying to find/parse config file at '{}'".format(conf_file)
        )
        sys.exit(1)

    sys.exit(0)
