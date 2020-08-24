
class PrimeImplicantTable(object):
    """ Prime implicant table constructor and associated methods for
    reducing prime implicants."""

    def __init__(self, prime_implicants, primitive_exprs):

        self.PI, self.PE = range(2)  # flags for the forms that the
                                     # prime implicant table can take:
                                     # PI for prime implicants as
                                     # keys, PE for primitive
                                     # expressions as keys

        # construct prime implicant table with primitive expressions
        # as keys
        self.pit = {}
        for pe in primitive_exprs:
            self.pit[pe] = [ pi for pi in prime_implicants if is_subset(pi,pe) ]
        # and set pit form to pe
        self.form = self.PE

    def __repr__(self):
        return repr(self.pit)

    def _invert_dict(self, d):
        """Swap keys and values of dictionary; values can be compound
        objects (e.g., list of tuples)."""
        new = {}
        for key, values in d.items():
            for value in values:
                if value in new.keys():
                    new[value].append(key)
                else:
                    new[value] = [key]

        return new

    def pi(self):
        """Return prime implicant table with prime implicants as keys."""
        if self.form == self.PE:
            # convert
            self.pit = self._invert_dict(self.pit)
            # and set pit form
            self.form = self.PI
        return self.pit

    def pe(self):
        """Return prime implicant table with primitive expressions as keys."""
        if self.form == self.PI:
            # convert
            self.pit = self._invert_dict(self.pit)
            # and set pit form
            self.form = self.PE
        return self.pit

    def _del_pi(self, prime_implicant):
        """Delete prime implicant."""
        self.pi()
        del self.pit[prime_implicant]

    def _del_pe(self, primitive_expr):
        """Delete primitive expression."""
        self.pe()
        del self.pit[primitive_expr]

    def _essential_prime_implicants(self, essential_pis = None):
        """Identify essential prime implicants."""

        # essential_pis collects essential prime implicants across
        # recursions of function
        if essential_pis is None:
            essential_pis = set()

        # identify essential prime implicants (primitive expressions
        # covered by only a single prime implicant)
        epis = set([ pis[0] for pe, pis in self.pe().items() if len(pis) == 1 ])

        # if essential prime implicants are found, remove them and
        # corresponding primitive expressions from prime implicant
        # table and check to see if any other (secondary) essential
        # prime implicants have emerged
        if epis:
            essential_pis |= epis
            for epi in epis:
                # all we need to do is delete the covered primitive
                # expressions and the corresponding essential prime
                # implicant will be deleted along the way
                pes = self.pi()[epi]
                for pe in pes:
                    self._del_pe(pe)
            if self.pit:
                self._essential_prime_implicants(essential_pis)
        return essential_pis

    def _isdominated(self, x, y):
        """Is vector X dominated by vector Y?"""
        for values in self.pit[x]:
            if values not in self.pit[y]:
                out = False
                break
        else:
            out = True
        return out

    def _iscodominant(self, x, y):
        """Is vector X co-dominant with vector Y?"""

        # vectors are co-dominant with each other when they cover the
        # same elements (primitive exprs or prime implicants)

        iscodom = True
        # test to see if all values for X are covered by Y
        for value in self.pit[x]:
            if value not in self.pit[y]:
                iscodom = False
                break

        # if so, test to see if all values for Y are covered by X
        if iscodom:
            for value in self.pit[y]:
                if value not in self.pit[x]:
                    iscodom = False
                    break

        return iscodom

    def minimize(self):
        """Reduce prime implicants."""

        covers = set()  # collection of minimal set of prime
                        # implicants that cover all primitive
                        # expressions

        while True:
            starting_pit = self.pit

            # begin by extracting any essential prime implicants
            covers |= self._essential_prime_implicants()

            # eliminate primitive expressions that DOMINATE other
            # primitive expressions
            if self.pit:
                for pe1 in self.pe().keys():
                    for pe2 in self.pe().keys():
                        if pe1 is not pe2:
                            try:
                                if self._iscodominant(pe1, pe2):
                                    # if primitive expressions are
                                    # codominant with each other can
                                    # eliminate either one
                                    self._del_pe(pe1)
                                elif self._isdominated(pe1, pe2):
                                    self._del_pe(pe2)
                                elif self._isdominated(pe2, pe1):
                                    self._del_pe(pe1)
                            except KeyError:  # primitive expression was
                                pass          # deleted in a previous step

            # check for any essential prime implicants that may have emerged
            if self.pit:
                covers |= self._essential_prime_implicants()

            # eliminate prime implicants DOMINATED by other prime
            # implicants
            # 
            # we test for "proper" domination--prime implicants that
            # are dominated but not codominant.  Properly dominated
            # prime implicants are deleted; codominant prime
            # implicants are left in the table to be subjected to
            # additional iterations.  If codominant prime implicants
            # can't be eliminated, they are inserted as part of the
            # solution.  (Note that this is very different from what
            # Ragin's fs/QCA does.  When fs/QCA encounters codominant
            # prime implicants, it brings up the prime implicant table
            # and forces the user to choose which prime implicant to
            # retain and which to delete.  This inevitably confuses
            # even experienced users.  Instead, I defer the question.
            # In the consistency and coverage table, these solutions
            # will report 0% unique coverage.  Examination by the user
            # will reveal that these solutions correspond to the same
            # cases.  The user can then decide whether to retain both
            # solutions or discard one.)
            if self.pit:
                for pi1 in self.pi().keys():
                    for pi2 in self.pi().keys():
                        if pi1 is not pi2:
                            try:
                                if self._isdominated(pi1, pi2) and \
                                        not self._iscodominant(pi1, pi2):
                                    self._del_pi(pi1)
                                elif self._isdominated(pi2, pi1) and \
                                        not self._iscodominant(pi2, pi1):
                                    self._del_pi(pi2)
                            except KeyError:  # prime implicant was
                                pass          # deleted in a previous step

            # and check for essential prime implicants one last time
            if self.pit:
                covers |= self._essential_prime_implicants()

            # if we've exhausted the prime implicant table, we're done
            if not self.pit:
                return covers
            # we're also done if there's only a single row left in the
            # prime implicant table (since, by definition, it must be
            # included in the solution)
            elif len(self.pit) == 1:
                covers |= set(self.pi().keys())
                return covers
            # if the prime implicant table can't be reduced any more,
            # we've reduced as far as we can with these techniques.
            # if we want to [try to] reduce any further, will need to
            # apply a cyclic coversing solution; compare keys because
            # values can get out of order
            elif self.pit.keys().sort() == starting_pit.keys().sort():
                covers |= set(self.pi().keys())
                return covers
            # otherwise, try again
        
class TruthTable(dict):
    """Truth table object, API, and associated routines for reduction."""

    def __init__(self, indict, causal_conds, obs_crossover=None):
        # sanity check
        if len(indict) != 2**len(causal_conds):
            raise TruthTableConstructionError, 'Wrong number of rows for number of causal conditions'
        self.update(indict)
        self.causal_conds = causal_conds
        self.obs_crossover = obs_crossover
            # if an observation calculates to 0.5 membership in a
            # corner, it's neither "in nor out" or the corner (or,
            # alternatively, in multiple corners simultaneously).  The
            # user should recoded the fuzzy-set membership scores for
            # these observations.  We collect these observations here
            # for future reference.  Note that the sort order isn't
            # guaranteed (although they're probably in the same order
            # of the input dataset).  If you wanted them sorted, have
            # the calling program do it.


    def __str__(self, consist_flag='n/a', contra_flag='Con', rem_flag='Rem', imp_flag='I', no_obs_flag='-'): 
        # convert dictionary to list of lists to pass to pretty print

        # generate minimum truth table to use to sort rows properly
        # (this is cribbed from TruthTableFactory.from_dataset() and
        # maybe should be factored out as a separate function.)
        num_causal_conds = len(self.causal_conds)
        i = (2**num_causal_conds)//2
        j = 1
        mintt = []
        while i >= 1:
            mintt_col=([True] * i + [False] * i) * j
            mintt=mintt+[mintt_col]
            i = i//2
            j = j*2
        mintt = zip(*mintt)

        tt2 = []
        for cc in mintt:
            row = []
            # causal conditions
            for causal_cond in cc:
                row += [causal_cond]
            # number of observations; note that this value isn't
            # stored along with the truth table but is merely
            # calculated from the consistent and inconsistent
            # observations and provided as a convenience to the user.
            # But, what this means is that when reading a truth table
            # in from an external file, the truth table factory method
            # will need to discard this column.
            num_obs = len(self[cc][2][0]) + len(self[cc][2][1])
            row += [num_obs]
            # consistency
            if self[cc][0] is not None:
                consist = '%#0.2f' % (self[cc][0])
            else:
                consist = consist_flag
            row += [consist]
            # outcome
            if self[cc][1] is Contradiction:
                outcome = contra_flag
            elif self[cc][1] is Remainder:
                outcome = rem_flag
            elif self[cc][1] is Impossible:
                outcome = imp_flag
            else:
                outcome = self[cc][1]
            row += [outcome]
            # consistent observations
            if self[cc][2][0]:
                consist_obs = ''
                for ob in self[cc][2][0]:
                    consist_obs += ob + ';'
                row += [consist_obs.rstrip(';')]
            else:
                row += [no_obs_flag]
            # inconsistent observations
            if self[cc][2][1]:
                inconsist_obs = ''
                for ob in self[cc][2][1]:
                    inconsist_obs += ob + ';'
                row += [inconsist_obs.rstrip(';')]
            else:
                row += [no_obs_flag]
            tt2.append(row)
        # header
        header = self.causal_conds + ['N', 'Consist', 'Outcome', 'ObsConsist', 'ObsInconsist']
        tt2.insert(0, header)
        alignment = len(self.causal_conds) * 'l,' + 'r,r,r,r,r'
        return (pp(tt2, alignment, ' '))

    ## the following methods were useful during development but can
    ## probably be removed for production; for now, I'll just comment
    ## them out.

    ## def primitive_exprs(self): return self.reduce(simplify=0)
    ## def prime_implicants(self): return self.reduce(simplify=1)

    def causal_configs(self, outcome=None):
        """Return (a subset of) the causal configurations of the truth
        table.

        outcome is a sequence indicating which configurations to
        return.  If unset, return all.  Otherwise, outcome can take
        any combination of values from class Outcomes (i.e., True,
        False, Remainder, Contradiction, or Impossible) and will
        return corresponding configurations.
        """

        if outcome is None:
            causal_configs = self.keys()
        else:
            if not isinstance(outcome, (list,tuple,set)):  # cast outcome
                outcome = [outcome]                        # as sequence
            causal_configs = [ causal_config for (causal_config, value) 
                               in self.items() if value[1] in outcome ]
        return causal_configs

    def obs_consist(self, causal_config=None):
        """Return observations that conform to specified causal
        configuration and are consistent with sufficiency.

        causal_config is a sequence of True, False, and/or None
        elements.  causal_config may be an exact causal configuration
        (elements are True or False) or a superset (by including
        "Don't Cares" specified as None).  If causal_config is None,
        return all consistent observations.
        """

        obs = []
        if causal_config is None:
            for value in self.itervalues():
                for ob in value[2][0]: # consistent observations
                    obs.append(ob)
        else:
            for key, value in self.items():
                if is_subset(causal_config, key):
                    for ob in value[2][0]:  # consistent observations
                        obs.append(ob)
        obs.sort()
        return obs

    def obs_inconsist(self, causal_config=None):
        """Return observations that conform to specified causal
        configuration and are inconsistent with sufficiency.

        causal_config is a sequence of True, False, and/or None
        elements.  causal_config may be an exact causal configuration
        (elements are True or False) or a superset (by including
        "Don't Cares" specified as None).  If causal_config is None,
        return all consistent observations.
        """

        obs = []
        if causal_config is None:
            for value in self.itervalues():
                for ob in value[2][1]: # inconsistent observations
                    obs.append(ob)
        else:
            for key, value in self.items():
                if is_subset(causal_config, key):
                    for ob in value[2][1]:  # inconsistent observations
                        obs.append(ob)
        obs.sort()
        return obs

    def reduce(self, simplify=1):
        """Reduce truth table."""

        def prime_implicants(minterms):
            """Determination of prime implicants as described by Roth
            (1985)."""

            # note that in QCA, minterms are called "primitive
            # expressions"

            while len(minterms) > 1:  # if only one minterm, nothing to reduce
                working = set([])  # use of sets means that we don't worry
                to_drop = set([])  # about accumulating duplicate vectors
                for minterm1 in minterms:
                    for minterm2 in minterms:
                        if minterm1 is not minterm2:
                            diffs = 0
                            combined = []
                            for el1,el2 in zip(minterm1, minterm2):
                                if el1 != el2:
                                    diffs += 1
                                    combined.append(None)
                                else:
                                    combined.append(el1)
                            if diffs == 1:  
                                # vectors can be combined; add reduced
                                # vector to working and flag these
                                # vectors to be dropped
                                working.add(tuple(combined))
                                to_drop.add(minterm1)
                                to_drop.add(minterm2)
                            else:
                                # vectors can't be combined; add both
                                # to working
                                working.add(minterm1)
                                working.add(minterm2)

                # drop combined vectors from working list
                working.difference_update(to_drop)

                # we know that the truth table can't be reduced any
                # further if working.mat is the same as the input
                # matrix.  Ugly because it means that the procedure
                # will always be executed one more time than is
                # necessary.
                if working != minterms:
                    minterms = working
                else:
                    break

            # if all truth table rows are included as minterms, prime
            # implicants can't be extracted.  Setting the outcome for
            # one or more rows to False will solve the problem.
            if len(working) == 1:
                for prime_implicant in working:
                    if prime_implicant.count(None) == len(prime_implicant):
                        raise PrimeImplicantsNotFoundError, 'No prime implicants found; add negative cases?'
            return working

        #
        # reduction procedure
        #
        
        # simplify must be an integer between 0 and 3
        simplify = int(simplify)
        if simplify < 0 or simplify > 3:
            raise ValueError, "Simplify paramater is out of range: %s" % simplify
        
        # test for present of contradictions
        if self.causal_configs(outcome=Contradiction):
            raise ContradictionError, "Contradiction(s) present.  Cannot reduce truth table."
        if not self.causal_configs(outcome=True):
            raise NoPositiveTTRowError, 'No positive outcome row(s) in truth table.  Nothing to reduce.'
        primitive_exprs = self.causal_configs(True)
        # what level of reduction?
        if not primitive_exprs:  # no positive cases; therefore, no solution
            solutions = None
        elif simplify == 0 or len(primitive_exprs) == 1:
            solutions = primitive_exprs
        elif simplify == 1:  # reduce to prime implicants
            solutions = prime_implicants(primitive_exprs)
        else:  # reduce prime implicants
            if simplify == 2:  # don't use remainders as simplifying assumptions
                causal_configs = [ key for key, value in self.items() \
                                       if value[1] is True ]
            elif simplify == 3:  # use remainders as simplifying
                               # assumptions; cast remainders as true
                               # when constructing prime implicants
                               # but not when constructing primitive
                               # expressions
                causal_configs = [ key for key, value in self.items() \
                                       if (value[1] is True or \
                                       value[1] is Remainder) ]
            pit = PrimeImplicantTable(prime_implicants(causal_configs), \
                                          primitive_exprs)
            solutions = pit.minimize()

        # return table of solutions, with causal conditions as header
        # row; if reduction not possible, return None
        if solutions:
            return [tuple(self.causal_conds)] + list(solutions)
        else:
            return None

class TruthTableFactory(object):
    """Truth table constructors."""

    def from_csv(self, infile, consist_flag=None, contra_flag=None, rem_flag=None, imp_flag=None, no_obs_flag=None):
        """Construct truth table from plain text representation.

        This method constructs a truth table from a plain text
        representation, such as a CSV file or the output of
        TruthTable.__str__()

        infile is either a file name or a file-like object (e.g., a
        StringIO instance)

        consist_flag is a tuple of the various strings used to signal
        that the consistency column is not applicable (b/c the causal
        condition is a remainder).

        contra_flag is a tuple of the various strings used to signal
        that a row of the truth table is a contradiction.

        rem_flag is a tuple of the various strings used to signal that
        a row of the truth table is a remainder.

        imp_flag is a tuple of the various strings used to signal that a
        row of the truth table has been marked as impossible.

        no_obs_flag is a tuple of the various strings used to signal
        that the consistent or inconsistent column is empty."""

        # the following five _flag variables are tuples of the various
        # textual markers used to indicate something about a given row
        # of the truth table (e.g., that the outcome is a remainder or
        # that there aren't any inconsistent observations for this
        # row).  The goal here is to be "liberal in what we accept"
        # since the truth table file could be created in a number of
        # ways including by acq's suf, Excel or OpenOffice, or by
        # hand.  When adding a marker to the tuple, make sure to
        # document why.  And upcase everything for ease of comparison.

        # consistency is not applicable for remainders
        if consist_flag is None:
            consist_flag = ('','N/A')
        else:
            if not isinstance(consist_flag, tuple):
                msg = 'consist_flag must be a tuple: %s' % consist_flag
                raise TypeError, msg

        # contradictions
        if contra_flag is None:
            contra_flag = ('CON',)
        else:
            if not isinstance(contra_flag, tuple):
                msg = 'contra_flag must be a tuple: %s' % contra_flag
                raise TypeError, msg

        # remainders
        #
        # of the five outcomes--T, F, Contradiction, Remainder,
        # Impossible--it is most likely that the empty string would
        # indicate a remainder.  QCA convention is that a dash is used
        # to signal remainders.
        if rem_flag is None:
            rem_flag = ('','-','REM')
        else:
            if not isinstance(rem_flag, tuple):
                msg = 'rem_flag must be a tuple: %s' % rem_flag
                raise TypeError, msg

        # impossible conditions
        if imp_flag is None:
            imp_flag = ('IMP','I','X')
        else:
            if not isinstance(imp_flag, tuple):
                msg = 'imp_flag must be a tuple: %s' % imp_flag
                raise TypeError, msg

        # consistent and/or inconsistent column is empty
        #
        # TruthTable.__str__() signals empty columns with a dash
        # (primarily so that the output will play nicely with Unix
        # tools).  OpenOffice converts dashes to '-0' and '-0' to 0.
        if no_obs_flag is None:
            no_obs_flag = ('', '-', '-0', '0')
        else:
            if not isinstance(no_obs_flag, tuple):
                msg = 'no_obs_flag must be a tuple: %s' % no_obs_flag
                raise TypeError, msg

        tt = {}
        try:
            file_like_stream = open(infile)
        except TypeError:  # infile is a StringIO instance (not a filename)
            file_like_stream = infile
        indata = [row.split() for row in file_like_stream]
        # last 5 columns are: N, Consistency, Outcome, Consistent
        # observations, Inconsistent observations; the N column is
        # dropped as it isn't part of the truth table object, only the
        # string representation.
        header_len = len(indata[0])
        for row in indata[1:]:
            # sanity check
            if len(row) != header_len:
                raise QcaError, 'Truth table rows are of unequal length' 
            # Causal conditions can be True or False
            causal_conds = row[:-5]
            ccs = []
            for cond in causal_conds:
                try:
                    if cond.upper() == 'TRUE':
                        ccs.append(True)
                    elif cond.upper() == 'FALSE':
                        ccs.append(False)
                    elif float(cond) == 1:
                        ccs.append(True)
                    elif float(cond) == 0:
                        ccs.append(False)
                    else:
                        raise ValueError
                except ValueError:
                    raise ValueError, "Illegal value for causal condition: %s" % cond
            ccs = tuple(ccs)
            # Consistency column (can be between 0.0 and 1.0 or n/a)
            consist = row[-4].strip()
            try:
                if consist.upper() in consist_flag:
                    consist = None
                else:
                    consist = float(consist)
            except ValueError:
                raise ValueError, "Illegal value in consistency column: %s" % consist
            # Outcome column (can be Contradiction, Remainder,
            # Impossible, True, or False)
            outcome = row[-3].strip()
            try:
                if outcome.upper() in contra_flag:
                    outcome = Contradiction
                elif outcome.upper() in rem_flag:
                    outcome = Remainder
                elif outcome.upper() in imp_flag:
                    outcome = Impossible
                elif outcome.upper() == 'TRUE':
                    outcome = True
                elif outcome.upper() == 'FALSE':
                    outcome = False
                elif float(outcome) == 1:
                    outcome = True
                elif float(outcome) == 0:
                    outcome = False
                else:
                    raise ValueError
            except ValueError:
                raise ValueError, "Illegal value for outcome: %s" % outcome
                
            # Consistent obs, semicolon-delimited list; empty list if none
            consist_obs = [] if row[-2] in no_obs_flag else [row[-2]]
            # Inconsistent obs, semicolon-delimited; empty list if none
            inconsist_obs = [] if row[-1] in no_obs_flag else [row[-1]]
            # build dictionary entry
            tt[ccs] = [consist, outcome, (consist_obs, inconsist_obs)]
        return TruthTable(tt, causal_conds=indata[0][0:-5])

    def from_dataset(self, indata, freq_thresh=1, consist_thresh=0.5, consist_prop=0.0):
        """Construct truth table from QCA conformant dataset."""

        # sanity checks; also, cast params as numeric
        freq_thresh = int(freq_thresh)
        if freq_thresh < 0:
            raise ValueError, freq_thresh
        consist_thresh = float(consist_thresh)
        if consist_thresh < 0.5 or consist_thresh > 1.0:
            raise ValueError, consist_thresh
        consist_prop = float(consist_prop)
        if consist_prop < 0.0 or consist_prop > 1.0:
            raise ValueError, consist_prop
 
        # generate minimum truth table
        num_causal_conds = len(indata.causal_conds())
        i = (2**num_causal_conds)//2
        j = 1
        mintt = []
        while i >= 1:
            mintt_col=([True] * i + [False] * i) * j
            mintt=mintt+[mintt_col]
            i = i//2
            j = j*2
        mintt = zip(*mintt)

        # for each causal configuration in the truth table, compute
        # its degree of membership in that corner of the vector space.
        # See Ragin (2008, Ch7) and Rihoux and Ragin (2008, Ch5) for a
        # complete discussion of the algorithm.
        tt = {}
        obs_crossover = []
        for causal_config in mintt:
            sum_min_xy = 0
            sum_x = 0
            obs_consist = []
            obs_inconsist = []
            for obs, outcome_membership, obs_name in zip(indata.causal_memberships(), indata.outcome_memberships(), indata.obs()):
                # compute current observation's degree of membership
                # for the current row of the truth table (i.e.,
                # combination of causal conditions or corner of the
                # vector space).
                corner_membership=1
                for causal_cond, membership_score in zip(causal_config, obs):
                    # in the truth table, the absence of a condition
                    # is marked as FALSE.  Therefore, in order to
                    # measure the degree to which an observation does
                    # *not* belong to particular causal condition, we
                    # need negate its membership in that condition.
                    if causal_cond==False:
                        membership_score = 1-membership_score
                    # compute corner membership by anding the causal
                    # memberships together.
                    corner_membership = min(corner_membership, membership_score)
                if corner_membership > 0.5:
                    # identify consistent/inconsistent observations
                    outcome_consist = (min(corner_membership, outcome_membership))/corner_membership
                    if outcome_consist >= consist_thresh:
                        obs_consist.append(obs_name)
                    else:
                        obs_inconsist.append(obs_name)
                elif corner_membership == 0.5:
                    # observations on the crossover point get dropped
                    # by the routine; collect them to report back as
                    # warning
                    if obs_name not in obs_crossover:
                        obs_crossover.append(obs_name)
                sum_min_xy += min(corner_membership, outcome_membership)
                sum_x += corner_membership
                try:
                    outcome_consist = sum_min_xy/sum_x
                except ZeroDivisionError:
                    outcome_consist = 0

            num_consist = len(obs_consist)
            num_inconsist = len(obs_inconsist)
            num_obs = num_consist + num_inconsist
            if num_obs < freq_thresh:
                outcome = Remainder
                if num_obs == 0:
                    outcome_consist = None
            elif num_consist/num_obs < consist_prop and num_inconsist/num_obs < consist_prop:
                    outcome = Contradiction
            elif outcome_consist >= consist_thresh:
                outcome = True
            else:
                outcome = False
            tt[causal_config] = [outcome_consist, outcome,
                                        (obs_consist, obs_inconsist)]
    
        return TruthTable(tt, causal_conds=indata.causal_conds(), obs_crossover=obs_crossover)

def concov_suf(qcadata, tt, qcasolution):
    """Return formatted consistency/coverage table of sufficient conditons."""

    # format a causal configuration
    def fmtTerm(term, causal_conds):
        formatted = ''
        for el, cond in zip(term, causal_conds):
            if el is True:
                formatted += cond.upper() + '*'
            elif el is False:
                formatted += cond.lower() + '*'
        return formatted.rstrip('*')

    terms = qcasolution[1:]
    obs_names = qcadata.obs()
    causal_memberships = qcadata.causal_memberships()
    outcome_memberships = qcadata.outcome_memberships()
    causal_conds = qcadata.causal_conds()

    # compute each case's degree of membership for each term from the
    # reduced truth table; "terms" are the individual solutions from
    # the reduced truth table
    sol_memberships = None
    consistencies = []
    raw_coverages = []
    all_term_memberships = []
    for term in terms:
        term_memberships = []
        # loop through observations (both data and outcome) from
        # original dataset
        for obs_name, obs, outcome in zip(obs_names, causal_memberships, outcome_memberships):
            term_membership = 1
            # each term in the solution is made up of one or more
            # causal conditions; for each causal condition, get the
            # observation's membership score from the original
            # dataset.  Skip causal conditions that aren't part of
            # this solution (will be marked as "None").  Otherwise,
            # AND the scores together to compute the observation's
            # degree of membership in this term of solution.  (If the
            # condition is False, will need to invert score first.)
            for causal_cond, score in zip(term, obs):
                if causal_cond is True:
                    term_membership = min(term_membership, score)
                elif causal_cond is False:
                    term_membership = min(term_membership, 1 - score)
            obs_consist = consist_suf([term_membership], [outcome])
            term_memberships.append(term_membership)

        # compute term consistency 
        consistencies.append(consist_suf(term_memberships, outcome_memberships))

        # compute term raw coverage
        raw_coverages.append(cov_suf(term_memberships, outcome_memberships))

        # OR term memberships together to get an observations'
        # memberships in the solution (i.e., all terms).  for the
        # first term, there's nothing to compare againt, so simply
        # copy term memberships over.
        if not sol_memberships:
            sol_memberships = term_memberships[:]
        else:
            sol_memberships = [ max(x,y) for x,y in zip(sol_memberships,
                                                        term_memberships) ]

        # collect term memberships for later use in calculating unique
        # coverages
        all_term_memberships.append(term_memberships)

    # compute consistency and raw coverage for total solution
    sol_consistency = consist_suf(sol_memberships, outcome_memberships)
    sol_coverage = cov_suf(sol_memberships, outcome_memberships)

    # compute unique coverages for individual terms by computing
    # combined raw coverages for all other terms and subtracting that
    # value from the total solution coverage
    uniq_coverages = []
    for i in range(len(terms)):
        memberships_in_other_terms = [max(term_membership) for term_membership in zip(*[term_memberships for j,term_memberships in enumerate(all_term_memberships) if i!=j])]
        raw_cov_other_terms = cov_suf(memberships_in_other_terms, outcome_memberships)
        uniq_coverages.append(sol_coverage-raw_cov_other_terms)

    concov = [['Term', 'Consist', 'RawCov', 'UniqCov', 'ObsConsist', 'ObsInconsist']]
    for term, consistency, raw_coverage, uniq_coverage, solution in zip(terms, consistencies, raw_coverages, uniq_coverages, qcasolution[1:]):
        consist_obs = ''
        for ob in tt.obs_consist(solution):
            consist_obs += ob + ';'
        consist_obs = consist_obs.rstrip(';')
        inconsist_obs = ''
        for ob in tt.obs_inconsist(solution):
            inconsist_obs += ob + ';'
        inconsist_obs = inconsist_obs.rstrip(';')
        if not inconsist_obs:  # all observations can be consistent
            inconsist_obs = '-'
        concov.append([fmtTerm(term, causal_conds) + '+', consistency, raw_coverage, uniq_coverage, consist_obs, inconsist_obs])
    concov[len(concov)-1][0] = concov[len(concov)-1][0].rstrip('+')  # strip OR from last term
    concov.append(["Solution", sol_consistency, sol_coverage, 'NA', 'NA', 'NA'])
    return concov

def concov_nec(qcadata, nec_conds, consist_thresh, cov_thresh):
    """Return formatted consistency/coverage table of necessary conditions."""

    def named2logical(named_term, causal_conds):
        logical = [None] * len(causal_conds)
        for i, cond in enumerate(causal_conds):
            for term in named_term:
                if cond.upper() == term.upper():
                    logical[i] = True if term.isupper() else False
        return logical

    concov = {}
    fzmin = [1] * len(qcadata.obs())  # seed ANDed solution
    for nec_cond in nec_conds:
        # identify observations that are consistent with this
        # necessary condition
        consistent_observations = []
        fzmax = [0] * len(qcadata.obs())  # seed ORed solution
        for i, obs_name, obs, outcome in zip(range(len(fzmax)), qcadata.obs(), qcadata.causal_memberships(), qcadata.outcome_memberships()):
            term_membership = 0
            # each term in the solution is made up of one or more
            # causal conditions; for each causal condition, get the
            # observation's membership score from the original
            # dataset.  Skip causal conditions that aren't part of
            # this solution (will be marked as 'None').  Otherwise, OR
            # the scores together to compute the observation's degree
            # of membership in this term of the solution.  (If the
            # condition is False, will need to invert score first.)
            for causal_cond, score in zip(named2logical(nec_cond, qcadata.causal_conds()), obs):
                if causal_cond is True:
                    term_membership = max(term_membership, score)
                elif causal_cond is False:
                    term_membership = max(term_membership, 1 - score)
            fzmax[i] = max(fzmax[i], term_membership)
            obs_consist = consist_nec([term_membership], [outcome])
            if obs_consist >= consist_thresh:
                consistent_observations.append(obs_name)

            consist = consist_nec(fzmax, qcadata.outcome_memberships())
            cov = cov_nec(fzmax, qcadata.outcome_memberships())


        # build concov table and compute solution consistency and
        # coverage, first dropping any necessary conditions that don't
        # meet specified coverage threshold
        if cov >= cov_thresh:
            concov[tuple(nec_cond)] = [consist, cov, consistent_observations]

            for i, row in enumerate(fzmax):
                fzmin[i] = min(fzmin[i], row)

            sol_consist = consist_nec(fzmin, qcadata.outcome_memberships())
            sol_cov = cov_nec(fzmin, qcadata.outcome_memberships())

    if concov:

        # format concov table  (do we need to add a sorting function?)
        tbl = [['Term','Consist','Cov','Obs']]
        for key, value in concov.items():
            # format causal conditions
            formatted = ''
            for cond in key:
                formatted += cond + '+'
            formatted = formatted.rstrip('+')
            formatted = formatted + '*'
            # consistency and coverage; it doesn't make sense to
            # partition coverage for necessary conditions, so we don't
            # do that
            consist = value[0]
            cov = value[1]
            # format observations
            obs = ''
            for ob in value[2]:
                obs += ob + ';'
            obs = obs.rstrip(';')
            tbl.append([formatted, consist, cov, obs])
        tbl[len(tbl)-1][0] = tbl[len(tbl)-1][0].rstrip('*')  # strip AND from last term
        tbl.append(['Solution', sol_consist, sol_cov, 'NA'])

        return tbl
