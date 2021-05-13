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
from datetime import datetime
from json import dumps
import logging
from os import path
import sys

from appdirs import user_config_dir
from pub_checker.check_slots import check_available_slots
from utils.json_utils import read_json_file

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="cowin-cowboy",
        description="Checks for available vaccination slots via Co-WIN API",
    )
    parser.add_argument("-l", "--log", default=logging.getLevelName(logging.ERROR))
    parser.add_argument("-c", "--config")

    args = parser.parse_args()

    logger = logging.getLogger(__name__)

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
        locations = config.get("locations")
        if locations is not None:
            logger.info("Checking API for available centers...")
            available_centers = check_available_slots(datetime.now(), locations)
            print(dumps(available_centers, sort_keys=True, indent=2))
            logger.info("{} centers are available".format(len(available_centers)))
        else:
            logger.error('"locations" key not found in config')
            sys.exit(1)
    else:
        logger.error(
            "Error while trying to find/parse config file at '{}'".format(conf_file)
        )
        sys.exit(1)

    sys.exit(0)
