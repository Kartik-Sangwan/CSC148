"""
CSC148, Winter 2019
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from typing import Optional
from bill import Bill
from call import Call
from math import ceil

# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


# TODO: Implement the MTMContract, TermContract, and PrepaidContract
class TermContract(Contract):
    """
    A Term Contract for a phoneline.

    This is a subclass of class Contract.

    === Public Attributes ===

    start:
        The start date of this term contract.
    end:
        The ending date of this term contract.
    curr_month:
        The month of the current bill.
    curr_year:
        The year of the current bill.
    """
    start: datetime.date
    end: datetime.date
    curr_month: int
    curr_year: int
    # i don't think term_deposit is required as an attribute.

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        Contract.__init__(self, start)
        self.end_date = end
        self.curr_month = 0
        self.curr_year = 0

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # initialising the <bill> argument.
        # term deposit is only added if it is the first month of the contract.
        # figure out how to access this bills attribute from phoneline.
        # if (month, year) in
        self.curr_month = month
        self.curr_year = year
        if self.bill is None:
            bill.add_fixed_cost(TERM_DEPOSIT)
        bill.set_rates("TERM", TERM_MINS_COST)
        self.bill = bill

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # ask if we cancel at a fixed time or like this below anytime.
        # contract was cancelled before end_date.Hence deposit forteified.
        if datetime.date(self.curr_year, self.curr_month, 30) > self.end_date:
            self.start = None
            return self.bill.get_cost() - TERM_DEPOSIT
        else:
            self.start = None
            return self.bill.get_cost()

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        # 60 thing messed up
        if self.bill.free_min == TERM_MINS:
            self.bill.add_billed_minutes(ceil(call.duration/60.0))
            return

        if self.bill.free_min + ceil(call.duration/60.0) <= TERM_MINS:
            self.bill.add_free_minutes(ceil(call.duration/60.0))
        else:
            remainder_mins = self.bill.free_min + ceil(call.duration/60.0) - \
                                  TERM_MINS
            self.bill.add_free_minutes(TERM_MINS - self.bill.free_min)
            self.bill.add_billed_minutes(remainder_mins)


class MTMContract(Contract):
    """
    A Month-To-Month contract for a phoneline.

    This is a subclass of Contract.

    === Public Attributes ===

    start_date:
            The start_date for this MTM Contract.

    """
    start_date: datetime.date

    def __init__(self, start: datetime.date) -> None:
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # didnt use month year parameters
        # why MTM mins_cost is less than cost of term_mins.handout says oppsite.
        bill.set_rates("MTM", MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)
        self.bill = bill
        # cancel contract for this is same as the superclass contract.


class PrepaidContract(Contract):
    """
    A Prepaid Contract for a phoneline.

    PrepaidContract is a subclass of Contract.

    === Public Attribute ===

    start:
        The start_date for this MTM Contract.
    balance:
        The amount of money customer owes.Include credit as negative amount.

    """
    start: datetime.date
    balance: float

    def __init__(self, start: datetime.date, balance: float) -> None:
        Contract.__init__(self, start)
        self.balance = balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """
        Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # month year parameters no need.
        # cancel_contract and bill call are same a superclass contract.
        bill.set_rates("PREPAID", PREPAID_MINS_COST)
        if self.bill is None:
            bill.add_fixed_cost(-self.balance)

        if self.balance > -10.0:
            bill.add_fixed_cost(25.0)
            self.balance -= 25.0
        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration/60.0))
        self.balance += ceil(call.duration/60.0) * PREPAID_MINS_COST

    def cancel_contract(self) -> float:
        """
        Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        if self.bill.get_cost() >= 0:
            return self.bill.get_cost()
        else:
            return 0.0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
