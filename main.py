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

import argparse
import datetime
import json
import logging
import os

from appdirs import user_config_dir
from pub_checker.check_slots import check_available_slots


def read_config_file(conf_file=None):
    """Reads the config file, and returns the object
    :param conf_file: location of config file
    :type conf_file: os.PathLike
    :return: Decoded config file, as a dictionary
    :rtype: dict
    """
    if conf_file is None:
        appname = "cowin-cowboy"
        appauthor = "Colocasian"
        conf_dir = user_config_dir(appname, appauthor)
        conf_file = os.path.join(conf_dir, "config.json")

    if os.path.isfile(conf_file):
        try:
            with open(conf_file) as conf_fp:
                config = json.load(conf_fp)
                return config
        except json.JSONDecodeError:
            logging.warning("could not decode config file '{}'".format(conf_file))
        except IOError:
            logging.warning("could not open file '{}'".format(conf_file))
    else:
        logging.warning("no file found at '{}'".format(conf_file))

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="cowin-cowboy",
        description="Checks for available vaccination slots via Co-WIN API",
    )
    log_choices = [
        logging.getLevelName(level)
        for level in [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
    ]
    parser.add_argument("-l", "--log", choices=log_choices)
    parser.add_argument("-c", "--config")

    args = parser.parse_args()

    if args.log is None:
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=getattr(logging, args.log.upper()))

    logging.info("Parsing config file...")
    config = read_config_file(conf_file=args.config)

    if config is not None:
        locations = config.get("locations")
        if locations is not None:
            available_centers = check_available_slots(
                datetime.datetime.now(), locations
            )
            print(json.dumps(available_centers, sort_keys=True, indent=2))
            print("{} centers are available".format(len(available_centers)))
        else:
            logging.warning('"locations" key not found in config')
