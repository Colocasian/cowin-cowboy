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

from json import JSONDecodeError
import logging
from typing import List
from zoneinfo import ZoneInfo

from pub_checker import pub_api_session


def _date_to_string(date):
    """Converts a datetime object to a string compatible with the Co-WIN
    API.
    Converts the timezone to Asia/Kolkata if `date.tz` is not `None`.

    :param date: the datetime instance
    :type date: datetime.datetime

    :return: Date string in DD-MM-YYYY format
    :rtype: str
    """
    date_format = "%d-%m-%Y"
    if date.tzinfo is not None:
        return date.astimezone(ZoneInfo("Asia/Kolkata")).strftime(date_format)
    return date.strftime(date_format)


def _check_for_pincode(date_str, pincode):
    """Returns a list of available centers based on the PIN code.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param pincode: PIN code to query
    :type pincode: str

    :return: A dictionary of center ID -> center details
    :rtype: dict[int, dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByPin"

    r = pub_api_session.get(endpoint, params={"pincode": pincode, "date": date_str})
    if r.ok:
        try:
            center_list = r.json().get("centers", [])
            return {center["center_id"]: center for center in center_list}
        except JSONDecodeError:
            logging.warning(
                "error while decoding JSON for pincode '{}'".format(pincode)
            )
    else:
        logging.warning(
            "HTTP status code {}: error response for pincode '{}'".format(
                r.status_code, pincode
            )
        )

    return {}


def _check_for_district(date_str, district_id):
    """Returns a list of available centers based on the district ID.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param district_id: District ID to query
    :type district_id: int

    :return: A dictionary of center ID -> center details
    :rtype: dict[int, dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByDistrict"

    r = pub_api_session.get(
        endpoint, params={"district_id": district_id, "date": date_str}
    )
    if r.ok:
        try:
            center_list = r.json().get("centers", [])
            return {center["center_id"]: center for center in center_list}
        except JSONDecodeError:
            logging.warning(
                "error while decoding JSON for district ID {}".format(district_id)
            )
    else:
        logging.warning(
            "HTTP status code {}: error response for district ID {}".format(
                r.status_code, district_id
            )
        )

    return {}


def _check_for_center(date_str, center_id):
    """Returns a list of available centers based on the district ID.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param center_id: District ID to query
    :type center_id: int

    :return: A dictionary of center ID -> center details
    :rtype: Optional[dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByCenter"

    r = pub_api_session.get(endpoint, params={"center_id": center_id, "date": date_str})
    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            logging.warning(
                "error while decoding JSON for center ID {}".format(center_id)
            )
    else:
        logging.warning(
            "HTTP status code {}: error response for center ID {}".format(
                r.status_code, center_id
            )
        )

    return None


def check_available_slots(date, pincodes=None, district_ids=None, center_ids=None):
    """Returns a dict of available vaccination centers for a given week

    :param date: The first day of the week to check
    :type date: datetime.datetime
    :param pincodes: List of PIN codes to check
    :type pincodes: List[str]
    :param district_ids: List of district IDs to check
    :type district_ids: List[int]
    :param center_ids: List of center IDs to check
    :type center_ids: List[int]

    :return: A dictionary of center ID -> center details
    :rtype:  dict[int, dict]
    """
    center_dict = {}
    date_str = _date_to_string(date)

    if pincodes is not None:
        for pincode in pincodes:
            center_dict.update(_check_for_pincode(date_str, pincode))

    if district_ids is not None:
        for district_id in district_ids:
            center_dict.update(_check_for_district(date_str, district_id))

    if center_ids is not None:
        for center_id in center_ids:
            if center_id not in center_dict:
                center_details = _check_for_center(date_str, center_id)
                if center_details is not None:
                    center_dict[center_id] = center_details

    return center_dict
