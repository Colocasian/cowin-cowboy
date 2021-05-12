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

from typing import List
from utils.api_utils import (
    date_to_string,
    check_for_pincode,
    check_for_district,
    check_for_center,
)

from pub_checker import pub_api_session


def check_available_slots(date, pincodes=None, district_ids=None, center_ids=None):
    """Returns a dict of available vaccination centers for a given week

    :param date: The first day of the week to check
    :type date: datetime.datetime
    :param pincodes: List of PIN codes to check
    :type pincodes: List[str]
    :param district_ids: List of district IDs to check
    :type district_ids: List[int]
    :param center_ids: List of center IDs to check. Note: Center API is
                       just a draft as of now, API request will return
                       '401 Forbidden: Unauthorised access!'
    :type center_ids: List[int]

    :return: A dictionary of center ID -> center details
    :rtype:  dict[int, dict]
    """
    center_dict = {}
    date_str = date_to_string(date)

    if pincodes is not None:
        for pincode in pincodes:
            center_dict.update(check_for_pincode(date_str, pincode, pub_api_session))

    if district_ids is not None:
        for district_id in district_ids:
            center_dict.update(
                check_for_district(date_str, district_id, pub_api_session)
            )

    if center_ids is not None:
        for center_id in center_ids:
            if center_id not in center_dict:
                center_details = check_for_center(date_str, center_id, pub_api_session)
                if center_details is not None:
                    center_dict[center_id] = center_details

    return center_dict
