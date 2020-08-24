# acqlib

# Copyright (c) 2011--2014 Christopher Reichert and Claude Rubinson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import sys
import signal
import logging
import itertools
import md5

from libfsqca import fznot, QcaDataset, concov_nec


class InvalidTruthTableElement( Exception ):
    """ Marks a cells contents as invalid in a truth table. """
    def __init__( self, val ):
        super( InvalidTruthTableElement, self ).__init__()
        self.value = val
    def __str__( self ):
        return repr( self.value )


def errorDlg(msg):
    errorMessage = QErrorMessage()
    errorMessage.showMessage( msg )
    errorMessage.exec_()


def reduceNecConcov(qcadata, consist_thresh, cov_thresh, causal_conds):
    """ Returns a concov_nec object """
    # construct new dataset with negated causal conditions
    with_negated=[['Cases'] + [cc.upper() for cc in qcadata.causal_conds()] + 
                  [cc.lower() for cc in qcadata.causal_conds()] + 
                  [qcadata.outcome()]]
    for obs_name, memberships, outcome_membership in \
            zip(qcadata.obs(),
                [cms + fznot(cms) for cms in qcadata.causal_memberships()],
                qcadata.outcome_memberships()):
        with_negated.append([obs_name] + memberships + [outcome_membership])
    qcadata_wn=QcaDataset(indata=with_negated)
    
    nec_conds = []
    if len( causal_conds) > 0:
        # if argument list is empty, test all possible combinations of conds
        causal_conditions = qcadata_wn.causal_conds()
        for i in range(1, len(causal_conditions)+1):
            # make sure to keep processing pending events in the event loop
            QCoreApplication.processEvents()
            test_conditions = itertools.combinations(causal_conditions, i)
            for condition in test_conditions:
                for nec_cond in nec_conds:  # ignore supersets of found
                                            # necessary conditions (e.g.,
                                            # if 'A' is a necessary
                                            # condition, 'A+B' is as well)
                    if set(nec_cond) < set(condition):
                        break
                else:
                    # ignore combinations with tautologies (e.g., A and a)
                    condition_upper = [term.upper() for term in condition]
                    for term in condition_upper:
                        if condition_upper.count(term) > 1:
                            break
                    else:
                        # test if this condition is a necessary condition
                        if qcadata_wn.isnec(condition, consist_thresh):
                            nec_conds.append(condition)
    return (concov_nec(qcadata, nec_conds, consist_thresh, cov_thresh))

