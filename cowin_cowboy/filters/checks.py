# checks.py -- common checks for filters module
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

__all__ = ["is_valid_session", "is_valid_center"]

from cowin_cowboy.utils.api_utils import _logger, FeeType


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
