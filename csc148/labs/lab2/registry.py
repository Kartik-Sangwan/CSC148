"""RACE REIGSTRY """

from __future__ import annotations
from typing import List


class Participant:
    """ A race registry of participants in a 5K run.

        ==== ATRIBUTES ===
        name: the name of the participant
        email: the email address of the participant
        speed_cat: the speed category of the participant

        === Sample Usage ===

        creating a participant
        >>> p = Participant('Gerhard', 'gerhard123@gmail.com', 'under 40')
        >>> p.name
        'Gerhard'
        >>> p.email
        'gerhard123@gmail.com'
        >>> p.speed_cat
        'under 40'
        >>> p.change_speed_cat('under 30')
        >>> p.speed_cat
        'under 30'
    """

    name: str
    email: str
    speed_cat: str

    def __init__(self, name: str, email_id: str, speed_cat: str) -> None:
        """Initialize a participant of the race.
        """
        self.name = name
        self.email = email_id
        self.speed_cat = speed_cat

    def change_email(self, new_email: str) -> None:
        """Change the email address of the participant to new_email.
        """
        self.email = new_email

    def change_speed_cat(self, new_scat: str) -> None:
        """Change the speed category of the participant to new_scat.
        """
        self.speed_cat = new_scat


class RaceRegistry:
    """
    A race registry for the 5K run.

    == ATTRIBUTES ==
    participants: A list of all the particiapnts in the 5K run.

    == Sample Usage ==

    >>> p = Participant('Gerhard', 'gerhard123@gmail.com', 'under 40')
    >>> q = Participant('Tom', 'tom123@gmail.com', 'under 30')
    >>> r = Participant('Toni', 'toni123@gmail.com', 'under 20')
    >>> s = Participant('Margot', 'margot123@gmail.com', 'under 30')
    >>> R = RaceRegistry([p, q, r, s])
    >>> R.runners_specific_cat('under 30')
    ['Tom', 'Margot']
    >>> R.find_runner_cat(r)
    'under 20'
    """

    participants: List[Participant]

    def __init__(self, participants: List[Participant]) -> None:
        """Initialise a new race registry with the participants list given.
        """
        self.participants = participants

    def find_runner_cat(self, runner: Participant) -> str:
        """Find the speed category of a runner in the race.
        """
        for p in self.participants:
            if p == runner:
                return runner.speed_cat

        return 'participant not found'

    def runners_specific_cat(self, cat: str) -> List[str]:
        """Returns a list of the participants in the given running category.
        """
        lst = []
        for p in self.participants:
            if p.speed_cat == cat:
                lst.append(p.name)
        return lst


if __name__ == '__main__':
    import doctest
    doctest.testmod()
