"""
Assignment 0 starter code
CSC148, Winter 2019
Diane Horton and Jacqueline Smith

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jacqueline Smith, and Bogdan Simion

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Diane Horton, Jacqueline Smith, and Bogdan Simion
"""
from datetime import date
from typing import Dict, Tuple, List, Set, Optional, IO


class Election:
    """Data for a single election in a parliamentary democracy.

    === Private Attributes ===
    _d: the date of this election.
    _ridings: all ridings for which any votes have been recorded in this
        election.
    _parties: all parties for which any votes have been recorded in this
        election.
    _results: the vote counts for this election.  Each key is the name of a
        riding, and its value is a dictionary of results for that one riding.
        Each of its keys, in turn, is the name of a party, and the associated
        value is the number of votes earned by that party in that riding.

    === Representation Invariants ==
    For all strings s, s in self._ridings iff s in self._results.
    For all strings s, s in self._parties iff s in self._results[r] for some r

    === Sample Usage ===
    >>> e = Election(date(2000, 2, 8))
    >>> e.update_results('r1', 'ndp', 1234)
    >>> e.update_results('r1', 'lib', 1345)
    >>> e.update_results('r1', 'pc', 1456)
    >>> e.riding_winners('r1')
    ['pc']
    >>> e.update_results('r2', 'pc', 1)
    >>> e.popular_vote() == {'ndp': 1234, 'lib': 1345, 'pc': 1457}
    True
    >>> e.results_for('r1', 'lib')
    1345
    >>> e.party_seats() == {'ndp': 0, 'lib': 0, 'pc': 2}
    True
    """
    _d: date
    _ridings: List[str]
    _parties: List[str]
    _results: Dict[str, Dict[str, int]]

    def __init__(self, d: date) -> None:
        """Initialize a new election on date d and with no votes recorded so
        far.

        >>> e = Election(date(2000, 2, 8))
        >>> e._d
        datetime.date(2000, 2, 8)
        """
        self._d = d
        self._ridings = []
        self._parties = []
        self._results = {}

    def ridings_of(self) -> List[str]:
        """Return the ridings in which votes have been recorded in this
         election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.ridings_of()
        ['r1']
        >>> e.update_results('r2', 'ndp', 1)
        >>> e.ridings_of()
        ['r1', 'r2']
        """
        return self._ridings

    def update_results(self, riding: str, party: str, votes: int) -> None:
        """Update this election to reflect that in <riding>, <party> received
        <votes> additional votes.

        <riding> may or may not already have some votes recorded in this
        election.  <party> may or may not already have some votes recorded in
        this riding in this election.


        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.results_for('r1', 'ndp')
        1
        >>> e.update_results('r1', 'ndp', 1000)
        >>> e.results_for('r1', 'ndp')
        1001
        """
        if riding in self._results and party in self._results[riding]:
            self._results[riding][party] += votes
        elif riding in self._results and party not in self._results[riding]:
            self._results[riding][party] = votes
            if party not in self._parties:
                self._parties.append(party)
        else:
            self._results[riding] = {party: votes}
            self._ridings.append(riding)
            if party not in self._parties:
                self._parties.append(party)

    def read_results(self, instream: IO[str]) -> None:
        """Update this election with the results in instream.

        Precondition: instream is an open csv file, in the format defined
        in the A0 handout.
        """
        instream.readline()
        for line in instream:
            lst = line.split(',')
            riding, party, votes = lst[1][1:-1:], lst[13][1:-1], int(lst[17])
            self.update_results(riding, party, votes)

    def results_for(self, riding: str, party: str) -> Optional[int]:
        """Return the number of votes received in <riding> by <party> in
        this election.

        Return None if <riding> does not have any votes recorded in this
        election, or if it does, but <party> does not have any votes recorded
        in this riding in this election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1234)
        >>> e.update_results('r1', 'lib', 1345)
        >>> e.update_results('r1', 'pc', 1456)
        >>> e.update_results('r2', 'pc', 1)
        >>> e.results_for('r1', 'pc')
        1456
        >>> e.results_for('r2', 'pc')
        1
        """
        if riding not in self._results:
            return None
        elif party not in self._results[riding]:
            return None
        else:
            return self._results[riding][party]

    def riding_winners(self, riding: str) -> List[str]:
        """Return the winners, in <riding>, of this election.

        The winner is the party or parties that received the most votes in
        total.  (There may have been a tie.)  The return value is a list so
        that, in the case of ties, we can return a list of election_winners.
        If there is no tie, the length of the returned list is 1.

        Precondition: <riding> has at least 1 vote recorded in this election.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.riding_winners('r1')
        ['pc']
        """
        winners = []
        max_val = max(self._results[riding].values())
        for party in self._results[riding]:
            if self._results[riding][party] == max_val:
                winners.append(party)
        return winners

    def popular_vote(self) -> Dict[str, int]:
        """Return the total number of votes earned by each party, across
        all ridings, in this election.

        Include all parties that have at least one vote recorded in at least
        one riding.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'pc', 4)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.popular_vote() == {'ndp': 8, 'lib': 7, 'pc': 7, 'green': 6}
        True
        """
        dic = {}
        for riding in self._results:
            for party in self._results[riding]:
                if self._results[riding][party] > 0 and party not in dic:
                    dic[party] = self._results[riding][party]
                elif self._results[riding][party] > 0:
                    dic[party] += self._results[riding][party]
        return dic

    def party_seats(self) -> Dict[str, int]:
        """Return the number of ridings that each party won in this election.

        Include all parties that have at least one vote recorded in at least
        one riding.  If there was a tie in a riding, it doesn't contribute to
        the seat count for any of the parties that tied in that riding.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'pc', 4)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.party_seats() == {'pc': 1, 'ndp': 1, 'lib': 0, 'green': 0}
        True
        """
        dic = {}
        for riding in self._results:
            winners = self.riding_winners(riding)
            if len(winners) == 1 and winners[0] not in dic:
                dic[winners[0]] = 1
            elif len(winners) == 1 and winners[0] in dic:
                dic[winners[0]] += 1
        for riding in self._results:
            for party in self._results[riding]:
                if party not in dic and self._results[riding][party] != 0:
                    dic[party] = 0
        return dic

    def election_winners(self) -> List[str]:
        """Return the party (or parties, in the case of a tie) that won the
        most seats in this election.

        If no votes have been recorded in any riding in this election,
        return the empty list.

        >>> e = Election(date(2000, 2, 8))
        >>> e.update_results('r1', 'ndp', 1)
        >>> e.update_results('r1', 'lib', 2)
        >>> e.update_results('r1', 'pc', 3)
        >>> e.update_results('r2', 'lib', 5)
        >>> e.update_results('r2', 'green', 6)
        >>> e.update_results('r2', 'ndp', 7)
        >>> e.update_results('r2', 'pc', 8)
        >>> e.election_winners()
        ['pc']
        """
        election_winners = []
        seats_dic = self.party_seats()
        max_seats = max(seats_dic.values())
        votes_cast = 0
        for riding in self._results:
            if sum(self._results[riding].values()) > 0:
                votes_cast = 1
        for party in seats_dic:
            if seats_dic[party] == max_seats:
                election_winners.append(party)
        if votes_cast == 0:
            return []
        else:
            return election_winners


class Jurisdiction:
    """The election history for a jurisdiction that is a parliamentary
    democracy.


    === Private Attributes ===
    _name: the name of this jurisdiction.
    _history: the election history for this jurisdiction.  Each key is a date,
        and its value holds the results of an election that was held on that
        date.

    === Representation Invariants ==
    None.

    === Sample Usage ===
    # See the method docstrings for sample usage.
    """
    _name: str
    _history: Dict[date, Election]

    def __init__(self, name: str) -> None:
        """Initialize this jurisdiction, with no elections so far.

        >>> country = Jurisdiction('Canada')
        >>> country._name
        'Canada'
        >>> country._history
        {}
        """
        self._name = name
        self._history = {}

    def read_results(self, year: int, month: int, day: int, instream: IO[str]) \
            -> None:
        """Read and record results for an election in this jurisdiction.

        If there are already some results stored for an election on this date,
        add to them.
        """
        d = date(year, month, day)
        e = Election(d)
        e.read_results(instream)
        if d not in self._history:
            self._history[d] = e
        else:
            self._history[d].read_results(instream)

    def party_wins(self, party: str) -> List[date]:
        """Return a list of all dates on which <party> won
        an election in this jurisdiction.

        If the party tied for most seats in an election, include that date
        in the result.

        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 2)
        >>> e1.update_results('r1', 'pc', 3)
        >>> e1.update_results('r2', 'lib', 10)
        >>> e1.update_results('r2', 'pc', 20)
        >>> e1.update_results('r3', 'ndp', 200)
        >>> e1.update_results('r3', 'pc', 100)
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 10)
        >>> e2.update_results('r1', 'lib', 20)
        >>> e2.update_results('r2', 'lib', 50)
        >>> e2.update_results('r2', 'pc', 5)
        >>> e3 = Election(date(2008, 6, 1))
        >>> e3.update_results('r1', 'ndp', 101)
        >>> e3.update_results('r1', 'lib', 102)
        >>> e3.update_results('r2', 'ndp', 1001)
        >>> e3.update_results('r2', 'lib', 1002)
        >>> j = Jurisdiction('Canada')
        >>> j._history[date(2000, 2, 8)] = e1
        >>> j._history[date(2004, 5, 16)] = e2
        >>> j._history[date(2008, 6, 1)] = e3
        >>> j.party_wins('lib')
        [datetime.date(2004, 5, 16), datetime.date(2008, 6, 1)]
        """
        dates_won = []
        for d in self._history:
            if party in self._history[d].election_winners():
                dates_won.append(d)
        return dates_won

    def party_history(self, party: str) -> Dict[date, float]:
        """Return this party's percentage of the popular vote
        in each election in this jurisdiction's history.

        Each key in the result is a date on which there was an election in
        this jurisdiction.  Its value is the percentage of the popular vote
        earned by party in that election.

        >>> j = Jurisdiction('Canada')
        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 2)
        >>> e1.update_results('r1', 'pc', 3)
        >>> e1.update_results('r2', 'pc', 4)
        >>> e1.update_results('r2', 'lib', 5)
        >>> e1.update_results('r2', 'green', 6)
        >>> e1.update_results('r2', 'ndp', 7)
        >>> e1.popular_vote() == {'ndp': 8, 'lib': 7, 'pc': 7, 'green': 6}
        True
        >>> j._history[date(2000, 2, 8)] = e1
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 40)
        >>> e2.update_results('r1', 'lib', 5)
        >>> e2.update_results('r2', 'lib', 10)
        >>> e2.update_results('r2', 'pc', 20)
        >>> e2.popular_vote() == {'ndp': 40, 'lib': 15, 'pc': 20}
        True
        >>> j._history[date(2004, 5, 16)] = e2
        >>> j.party_history('lib') == {date(2000, 2, 8): 0.25, \
        date(2004, 5, 16): 0.2}
        True
        """
        result = {}
        for d in self._history:
            dic = self._history[d].popular_vote()
            if party in dic:
                percentage = dic[party]/sum(dic.values())
                result[d] = percentage
            else:
                result[d] = 0
        return result

    def riding_changes(self) -> List[Tuple[Set[str], Set[str]]]:
        """Return the changes in ridings across elections in this jurisdiction.

        Include a tuple for each pair of elections, in order by date.
        The tuple should contain, first, a list of ridings that were removed
        between these two elections, and then a list of ridings that were
        added.

        Precondition: There is at least one election recorded for this
        jurisdiction.

        >>> j = Jurisdiction('Canada')
        >>> e1 = Election(date(2000, 2, 8))
        >>> e1.update_results('r1', 'ndp', 1)
        >>> e1.update_results('r1', 'lib', 1)
        >>> e1.update_results('r1', 'pc', 1)
        >>> e1.update_results('r2', 'pc', 1)
        >>> e1.update_results('r2', 'lib', 1)
        >>> e1.update_results('r2', 'green', 1)
        >>> e1.update_results('r2', 'ndp', 1)
        >>> j._history[date(2000, 2, 8)] = e1
        >>> e2 = Election(date(2004, 5, 16))
        >>> e2.update_results('r1', 'ndp', 1)
        >>> e2.update_results('r3', 'pc', 1)
        >>> j._history[date(2004, 5, 16)] = e2
        >>> j.riding_changes() == [({'r2'}, {'r3'})]
        True
        """
        lst = []
        temp = {}
        if len(self._history) == 1:
            return []
        else:
            for key in sorted(self._history):
                temp[key] = self._history[key]
            self._history = temp
            for i in range(len(self._history)):
                if i != len(self._history) - 1:
                    lst_e = list(self._history.values())
                    e1, e2 = lst_e[i], lst_e[i + 1]
                    e1_ridings = set(e1.ridings_of())
                    e2_ridings = set(e2.ridings_of())
                    removed = e1_ridings.difference(e2_ridings)
                    added = e2_ridings.difference(e1_ridings)
                    lst.append((removed, added))
            return lst


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['Election.read_results', 'Jurisdiction.read_results'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'datetime', 'typing'
        ],
        'max-attributes': 15
    })

    import doctest
    doctest.testmod()

    # An example of reading election results from a file.
    # c = Jurisdiction('Canada')
    # c.read_results(2015, 2, 3, open('../data/parkdale-highpark.csv'))
    # c.read_results(2015, 2, 3, open('../data/nunavut.csv'))
    # c.read_results(2015, 2, 3, open('../data/labrador.csv'))
