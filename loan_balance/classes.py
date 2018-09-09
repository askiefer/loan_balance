
"""
This module provides Loan, Facility, and Covenant classes
"""

class Loan:
    """Models a loan object

    Args:
        A dictionary representing a loan
    """
    def __init__(self, row):
        self.interest_rate = row['interest_rate']
        self.amount = row['amount']
        self.id = row['id']
        self.default_likelihood = row['default_likelihood']
        self.state = row['state']
  

class Facility:
    """Models a facility object

    Args:
        A dictionary representing a facility
    """
    def __init__(self, row):
        self.amount = row['amount']
        self.interest_rate = row['interest_rate']
        self.id = row['id']
        self.bank_id = row['bank_id']
        self.expected_yield = 0

    def amount_remaining(self, loan):
        return to_float(self.amount) - to_float(loan.amount)

    def has_amount(self, loan):
        return self.amount_remaining(loan) > 0

    def calculate_amount_remaining(self, loan):
        self.amount = self.amount_remaining(loan)

    def calculate_expected_yield(self, loan):
        amount = to_float(loan.amount)
        interest_rate = to_float(loan.interest_rate)
        default_likelihood = to_float(loan.default_likelihood)
        expected_yield = ((1 - default_likelihood) * interest_rate) * amount
        expected_yield -= (default_likelihood * amount)
        expected_yield -= (to_float(self.interest_rate) * amount)
        self.expected_yield += expected_yield


class Covenant:
    """Models a covenant object

    Args:
        A dictionary representing a covenant
    """
    def __init__(self, row):
        self.facility_id = row['facility_id']
        self.max_default_likelihood = row['max_default_likelihood']
        self.bank_id = row['bank_id']
        self.banned_state = row['banned_state']

    def banned_facility_id(self, facility):
        return self.facility_id == facility.id

    def above_default(self, loan):
        return self.max_default_likelihood < loan.default_likelihood

    def banned_state(self, loan):
        return self.banned_state == loan.state


def to_float(val):
    try:
        val = float(val)
    except (ValueError, TypeError) as e:
        print(e)
    return val
