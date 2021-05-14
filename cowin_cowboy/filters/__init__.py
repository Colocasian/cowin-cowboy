# filters/__init__.py -- filters module, to filter vaccination slots
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

__all__ = ["filter_available_centers"]

from copy import deepcopy
from logging import getLogger

from cowin_cowboy.utils.api_utils import is_valid_center

_logger = getLogger(__name__)


def filter_available_centers(centers, filters):
    """Returns a dict of the centers which satisfy the provided filters.
    Note: Even if `filters` is an empty dict, this function will remove
    all sessions with no available capacity.

    :param centers: the dictionary of center ID to center details
    :type centers: dict[int, dict]
    :param filters: a dictionary containing all the required filters
    :type filters: dict
    :return: dictionary of all centers which satisfy the given filters
    :rtype: dict
    """
    filtered_centers = {
        center_id: center
        for center_id, center in deepcopy(centers).items()
        if is_valid_center(center, filters)
    }
    return filtered_centers
