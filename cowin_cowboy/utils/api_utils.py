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
    "FeeType",
    "date_to_string",
    "check_for_pincode",
    "check_for_district",
    "check_for_center",
    "is_valid_session",
    "is_valid_center",
]

from enum import Enum, unique
from json import JSONDecodeError
from logging import getLogger
from zoneinfo import ZoneInfo

_logger = getLogger(__name__)


@unique
class FeeType(Enum):
    FREE = "Free"
    PAID = "Paid"


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
            _logger.warning(
                "Error while decoding JSON for PIN code '{}'".format(pincode)
            )
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


def is_valid_session(session, filters):
    """Helper function to check whether the given session is valid
    according to the provided filters.
    Note: It will remove all session with no capacity

    :param session: session details
    :type session: dict
    :param filters: filter to check session with
    :type filters: dict
    :return: whether the session is valid and satisfies the filters
    :rtype: bool
    """
    try:
        if session["available_capacity"] <= 0:
            return False

        if "age" in filters:
            if filters["age"] < session["min_age_limit"]:
                return False

        if "vaccine" in filters:
            if session["vaccine"].upper() not in [
                vac.upper() for vac in filters["vaccine"]
            ]:
                return False

    except KeyError:
        _logger.debug("Invalid session details, returning false")
        return False
    except TypeError:
        _logger.debug("Invalid type in some field")
        return False

    return True


def is_valid_center(center, filters):
    """Helper function to check whether the given center is valid
    according to the provided filters.
    Note: It will remove all session with no capacity

    :param center: center details
    :type center: dict
    :param filters: filter to check session with
    :type filters: dict
    :return: whether the session is valid and satisfies the filters
    :rtype: bool
    """
    try:
        if "feeType" in filters:
            fee_types_upper = [key.upper() for key in FeeType.__members__.keys()]
            if filters["feeType"].upper() in fee_types_upper:
                if filters["feeType"].upper() != center["fee_type"].upper():
                    return False

        def custom_session_filter(session):
            return is_valid_session(session, filters)

        filtered_session = list(filter(custom_session_filter, center["sessions"]))
        if not filtered_session:
            return False
        center["sessions"] = filtered_session
        if not center["sessions"]:
            return False

    except KeyError:
        _logger.warning("Invalid center details")
        return False
    except TypeError:
        _logger.warning("Invalid value type")
        return False

    return True
