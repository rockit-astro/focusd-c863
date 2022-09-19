#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by c863_focusd"""


class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2
    InvalidControlIP = 3

    PositionOutsideLimits = 6
    NotConnected = 7
    NotDisconnected = 8

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        3: 'error: command not accepted from this IP',
        6: 'error: requested position outside channel range',
        7: 'error: focuser is not connected',
        8: 'error: focuser is already connected',

        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with focus daemon',
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return f'error: Unknown error code {error_code}'


class FocuserStatus:
    """Status of the controller hardware"""
    Disabled, Initializing, Idle, Moving = range(4)

    _labels = {
        0: 'OFFLINE',
        1: 'INITIALIZING',
        2: 'IDLE',
        3: 'MOVING',
    }

    _colors = {
        0: 'red',
        1: 'yellow',
        2: 'default',
        3: 'yellow'
    }

    @classmethod
    def label(cls, status, formatting=False):
        """Returns a human readable string describing a status
           Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._labels and status in cls._colors:
                return f'[b][{cls._colors[status]}]{cls._labels[status]}[/{cls._colors[status]}][/b]'
            return '[b][red]UNKNOWN[/red][/b]'

        if status in cls._labels:
            return cls._labels[status]
        return 'UNKNOWN'
