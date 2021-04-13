# fuzzy - fuzzy number type

# Copyright (c) 2011--2012 Claude Rubinson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

class fz(object):
    """Fuzzy number type."""

    def __init__(self, value):
        self.value = float(value)
        if self.value < 0.0 or self.value > 1.0:
            raise ValueError, 'value for fz() must be between 0.0 and 1.0: %s' % value

    def __repr__(self):
        return 'fz(%s)' % self.value
    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return fz(max(self.value, other.value))
    def __mul__(self, other):
        return fz(min(self.value, other.value))
    def __invert__(self):
        return fz(1.0-self.value)

    def __float__(self):
        return self.value

