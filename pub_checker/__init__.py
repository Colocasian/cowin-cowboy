# pub_checker/__init__.py -- public API module
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

from requests_toolbelt import sessions
from requests_toolbelt.cookies.forgetful import ForgetfulCookieJar

from pub_checker.config import *

# Initialise a forgetful session with base URL
pub_api_session = sessions.BaseUrlSession(base_url=API_URL)
pub_api_session.headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
pub_api_session.cookies = ForgetfulCookieJar()
