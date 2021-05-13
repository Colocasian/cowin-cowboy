# api_utils.py -- utilities related to API use
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

__all__ = [
    "date_to_string",
    "check_for_pincode",
    "check_for_district",
    "check_for_center",
]

from logging import getLogger
from json import JSONDecodeError
from zoneinfo import ZoneInfo

_logger = getLogger(__name__)


def date_to_string(date):
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


def check_for_pincode(date_str, pincode, api_session):
    """Returns a list of available centers based on the PIN code.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param pincode: PIN code to query
    :type pincode: str
    :param api_session: An existing API session
    :type api_session: requests_toolbelt.sessions.BaseUrlSession

    :return: A dictionary of center ID -> center details
    :rtype: dict[int, dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByPin"

    params = {"pincode": pincode, "date": date_str}
    r = api_session.get(endpoint, params=params)
    if r.ok:
        try:
            center_list = r.json().get("centers", [])
            return {center["center_id"]: center for center in center_list}
        except JSONDecodeError:
            _logger.warning("Error while decoding JSON for PIN code '{}'".format(pincode))
            _logger.debug("Response:\n".format(r.content))
    else:
        _logger.warning(
            "HTTP status code {}: error response for PIN code '{}'".format(
                r.status_code, pincode
            )
        )
        _logger.debug("Response:\n".format(r.content))

    return {}


def check_for_district(date_str, district_id, api_session):
    """Returns a list of available centers based on the district ID.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param district_id: District ID to query
    :type district_id: int
    :param api_session: An existing API session
    :type api_session: requests.Session

    :return: A dictionary of center ID -> center details
    :rtype: dict[int, dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByDistrict"

    params = {"district_id": district_id, "date": date_str}
    r = api_session.get(endpoint, params=params)
    if r.ok:
        try:
            center_list = r.json().get("centers", [])
            return {center["center_id"]: center for center in center_list}
        except JSONDecodeError:
            _logger.warning(
                "Error while decoding JSON for district ID {}".format(district_id)
            )
            _logger.debug("Response:\n".format(r.content))
    else:
        _logger.warning(
            "HTTP status code {}: error response for district ID {}".format(
                r.status_code, district_id
            )
        )
        _logger.debug("Response:\n".format(r.content))

    return {}


def check_for_center(date_str, center_id, api_session):
    """Returns a list of available centers based on the district ID.

    :param date_str: The date as string, in DD-MM-YYYY
    :type date_str: str
    :param center_id: District ID to query
    :type center_id: int
    :param api_session: An existing API session
    :type api_session: requests.Session

    :return: A dictionary of center ID -> center details
    :rtype: Optional[dict]
    """
    endpoint = "v2/appointment/sessions/public/calendarByCenter"

    params = {"center_id": center_id, "date": date_str}
    r = api_session.get(endpoint, params=params)
    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            _logger.warning(
                "Error while decoding JSON for center ID {}".format(center_id)
            )
            _logger.debug("Response:\n".format(r.content))
    else:
        _logger.warning(
            "HTTP status code {}: error response for center ID {}".format(
                r.status_code, center_id
            )
        )
        _logger.debug("Response:\n".format(r.content))

    return None
