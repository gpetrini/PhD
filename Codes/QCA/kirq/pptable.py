# pptable - pretty print tables in Python

# pptable is a rewrite of Ryan Ginstrom's padnums module,
# available at
# http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/.
# In comparison to padnums, pptable is a bit more flexible and
# efficient.

# Copyright (c) 2010--2012 Claude Rubinson and Ryan Ginstrom

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import string

# constants
l = 'l'
r = 'r'

def _format_field(field, format=None, quote=None):
    """Format number using printf syntax or convert to string."""

    if not format:
        format = '%s'

    if isinstance(field, (bool,str)):
        formatted = str(field)
    else:
        try:
            formatted = format % field
        except (TypeError, ValueError), exc:
            msg = 'invalid string formatting specification: %s' % format
            exc.args = (msg,)
            raise

    if quote and any(map(lambda x: x in string.whitespace, formatted)):
        return '%s%s%s' % (quote,formatted,quote)
    else:
        return formatted

def _format_col(col, col_fmt, col_width, quote=None):
    """Align column and format field."""

    alignment, fmt = col_fmt
    if alignment == l:
        return _format_field(col, fmt, quote).ljust(col_width)
    elif alignment == r:
        return _format_field(col, fmt, quote).rjust(col_width)
    else:
        msg = 'invalid formatting specification: %s' % alignment
        raise Exception, msg

def pp(table, template=None, delim=' ', quote=None):
    """Pretty print a table, left/right padding for alignment.

    table is a rectangular list of lists, with each row having the
    same number of columns.

    template is a comma-delimited string where elements are of the
    form 'alignment[%printf]'; that is, a prefix 'l' or 'r',
    indicating whether to left or right justify that column,
    optionally followed by a printf formatting command.  If template
    is unspecified, the first column will be left justified and all
    other columns will be right justified.

    delim is the output delimiter; default is a single space

    quote is a string to quote fields with embedded spaces; default is
    to not quote."""

    num_cols = len(table[0])

    # default template has first column left justified and remaining
    # columns right justified
    if not template:
        fmt = [(l,None)] + [(r,None)] * (num_cols-1)
    # fmt is a list of tuples, indicating whether to left or right
    # justify and specifying number formatting
    else:
        fmt = [(col[0],col[1:]) for col in template.split(',')]

    # get max width of each column
    column_widths = []
    for col in range(num_cols):
        column_widths.append(max([len(_format_field(row[col],fmt[col][1],quote)) for row in table]))

    quotes = (quote,)*num_cols
    out = []
    for row in table:
        out.append(delim.join(map(_format_col, row, fmt, column_widths, quotes)))
    return '\n'.join(out)

if __name__=="__main__":
    table = [["", "taste", "life", "land speed"],
             ["spam", 300101, 4, 1003],
             ["eggs", 105, 'per capita', 42],
             ["lumberjacks", 13, False, 10]]

    print pp(table, quote='"')
