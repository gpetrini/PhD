# dataset - dataset class and constructors

# Copyright (c) 2012--2013 Claude Rubinson

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

import csv
import mimetypes
import sys
import xlrd
import openpyxl
import collections
import re
from pptable import *


class DatasetError(Exception):
    """Base class for exceptions in dataset module."""
    pass

class DuplicateValueError(DatasetError):
    """Exception raised when duplicate values are prohibited."""

    def __init__(self, values, msg='Duplicate value: '):
        self.values = values
        self.msg = msg

    def __str__(self):
        return self.msg + ', '.join(self.values)

class EmptyCellError(DatasetError):
    """Exception raised when empty data cells are prohibited."""
    pass

class RaggedDatasetError(DatasetError):
    """Exception raised when ragged dataset is prohibited."""
    pass

class SheetNotFoundError(DatasetError):
    """Exception raised when specified workbook sheet is not found."""
    pass

class FileTypeNotSupportedError(DatasetError):
    """Exception raised when user tried to read data from an
    unsupported format."""
    pass

class EmbeddedWhitespaceError(DatasetError):
    """Exception raised when the name of a variable or observation
    contains prohibited whitespace."""

    def __init__(self, values, msg='Whitespace prohibited in variable and observation names: '):
        self.values = values
        self.msg = msg

    def __str__(self):
        return self.msg + ', '.join(self.values)

class Dataset(list):
    """Dataset object and API.

    Structurally, a Dataset object is a list of lists (or tuples).
    The first row is column headers (variables) and the first column
    is row headers (observations).  Missing cells are prohibited."""

    def __init__(self, indata):

        list.__init__(self, indata)

        # whitespace is prohibited in variable and observation names
        whitespace = [var for var in self.vars() if re.search('\s', var)]
        if whitespace:
            raise EmbeddedWhitespaceError(whitespace, 'Whitespace prohibited in variable names: ')
        whitespace = [ob for ob in self.obs() if re.search('\s', ob)]
        if whitespace:
            raise EmbeddedWhitespaceError(whitespace, 'Whitespace prohibited in observation names: ')

        # check for duplicate column names
        vars_count = collections.Counter(self.vars())
        dupes = [var for var in vars_count if vars_count[var] > 1]
        if dupes:
            raise DuplicateValueError(dupes, 'Duplicate column name(s): ')

        # check for duplicate row names
        obs_count = collections.Counter(self.obs())
        dupes = [ob for ob in obs_count if obs_count[ob] > 1]
        if dupes:
            raise DuplicateValueError(dupes, 'Duplicate row name(s): ')

        # check for empty cells and/or ragged table
        row_lengths = []
        for row_num, row in enumerate(self):
            if not all(map(str,row)):
                raise EmptyCellError, 'Row %s' % row_num
            row_lengths.append(len(row))
        if min(row_lengths) < max(row_lengths):
            raise RaggedDatasetError

    def __str__(self):
        return pp(self)

    def vars(self):
        """Return names of variables as a list."""
        return self[0][1:]

    def obs(self):
        """Return names of observations as a list."""
        return [obs[0] for obs in self[1:]]

class DatasetFactory(object):
    """Dataset constructors."""

    def from_any(self, filename=None, file_type=None):
        """Construct dataset based on file extension, or by explicit
        specification.  If filename not specified, read from stdin."""

        if filename is None:
            return self.from_csv('/dev/stdin')
        else:
            # if file type specified, force
            if str(file_type).lower() in ('csv','text','ascii'):
                return self.from_csv(filename)
            elif str(file_type).lower() in ('xls','excel'):
                return self.from_xls(filename)
            # otherwise, check extension
            else:
                mimetype = mimetypes.guess_type(filename)[0]
                if mimetype == 'application/vnd.ms-excel':
                    return self.from_xls(filename)
                elif mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    return self.from_xlsx(filename)
                else:  # default to treating as plain text
                       # regardless of extension
                    return self.from_csv(filename)

    def from_csv(self, file_name='/dev/stdin'):
        """Construct dataset from CSV file."""

        # read csvfile into a list, so that we can navigate backwards
        # through the list (which isn't possible when reading stdin
        # via a pipe)
        csvdata = open(file_name).readlines()

        # sniff the delimiter from the second line of data so as to
        # skip the header row, which is more likely to include an
        # embedded space or other delimiter-like character as part of
        # a variable name, possibly confusing the sniffer.
        try:
            sample = csvdata[1]
        except IndexError:  # raised if csvfile has only 1 row
            if file_name == '/dev/stdin':
                raise DatasetError, 'Bad input on standard input stream'
            elif len(csvdata) == 1:
                raise DatasetError, 'Only one row in input file: %s' % file_name
            else:
                raise
        dialect = csv.Sniffer().sniff(sample)

        working = []
        row_lengths = []
        for row in csv.reader(csvdata, dialect, skipinitialspace=True):
            working.append([col.strip() for col in row])
        return Dataset(working)

    def from_xls(self, xlsfile, xlssheet=None):
        """Construct dataset from Excel 95-2003 (xls) file."""

        # open workbook
        wb = xlrd.open_workbook(xlsfile)

        # sheet can be specified by index or name; if not specified,
        # default to first sheet
        if xlssheet is None:
            sh = wb.sheet_by_index(0)
        else:
            if str(xlssheet).isdigit():
                try:
                    sh = wb.sheet_by_index(int(xlssheet))
                except IndexError:
                    raise SheetNotFoundError, xlssheet
            else:
                try:
                    sh = wb.sheet_by_name(str(xlssheet))
                except XLRDError:
                    raise SheetNotFoundError, xlssheet

        # read data, casting observation column to string
        return Dataset([str(sh.row_values(i)[0])]+sh.row_values(i)[1:] for i in range(sh.nrows))

    def from_xlsx(self, xlsxfile, xlsxsheet=None):
        """Construct dataset from Excel 2007/2010 OOXML (xlsx) file."""

        # open workbook
        try:
            wb = openpyxl.load_workbook(xlsxfile)
        except openpyxl.shared.exc.InvalidFileException:
            raise IOError, "[Errno 2] No such file or directory: '%s'" % xlsxfile

        # sheet can be specified by index or name; if not specified,
        # default to first sheet
        if xlsxsheet is None:
            sh = wb.get_active_sheet()
        else:
            if str(xlsxsheet).isdigit():
                try:
                    sheet_name = wb.get_sheet_names()[xlsxsheet]
                    sh = wb.get_sheet_by_name(sheet_name)
                except IndexError:
                    raise SheetNotFoundError, xlsxsheet
            else:
                sh = wb.get_sheet_by_name(sheet_name)
                if not sh:  # sh will be None if sheet doesn't exist
                    raise SheetNotFoundError, xlsxsheet

        # read data, casting observation column to string
        data = [[cell.value for cell in row] for row in sh.rows]
        # library converts empty cells to None; catch them
        for row_num, row in enumerate(data):
            if any(cell is None for cell in row):
                raise EmptyCellError, 'Row %s' % row_num
        return Dataset([[str(row[0])]+row[1:] for row in data])
        
if __name__ == '__main__':
    dsf = DatasetFactory()
    ds = dsf.from_any(sys.argv[1])
    print ds
