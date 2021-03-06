# check_slots.py -- checks for available slots via public API
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

__all__ = ["check_available_slots"]

from logging import getLogger

from cowin_cowboy.utils.api_utils import (
    date_to_string,
    check_for_pincode,
    check_for_district,
    check_for_center,
    merge_center_dicts,
)
from cowin_cowboy.pub_checker._api_session import pub_api_session

_logger = getLogger(__name__)


def check_available_slots(date_obj, locations):
    """Returns a dict of available vaccination centers for a given week

    :param date_obj: The first day of the week to check
    :type date_obj: datetime.date
    :param locations: A dictionary containing the list of PIN codes at
            key `pincodes`, list of district IDs at key
            `district_ids`, and list of center IDs at key
            `center_ids`. Note: Center API is just a draft as of now,
            API request will return '401 Forbidden: Unauthorised
            access!'
    :type locations: dict

    :return: A dictionary of center ID -> center details
    :rtype:  dict[int, dict]
    """
    center_dict = {}
    date_str = date_to_string(date_obj)
    _logger.info("Checking available slots for date {}".format(date_str))

    if locations is not None:
        pincodes = locations.get("pincodes", [])
        for pincode in pincodes:
            pin_dict = check_for_pincode(date_str, pincode, pub_api_session)
            merge_center_dicts(center_dict, pin_dict)

        district_ids = locations.get("district_ids", [])
        for district_id in district_ids:
            district_dict = check_for_district(date_str, district_id, pub_api_session)
            merge_center_dicts(center_dict, district_dict)

        center_ids = locations.get("center_ids", [])
        for center_id in center_ids:
            if center_id not in center_dict:
                center_details = check_for_center(date_str, center_id, pub_api_session)
                if center_details is not None:
                    center_dict[center_id] = center_details
            center_details = check_for_center(date_str, center_id, pub_api_session)
            if center_details is not None:
                merge_center_dicts(center_dict, {center_id: center_details})

    return center_dict
