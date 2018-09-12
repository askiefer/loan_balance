import csv
import os
from .classes import Loan, Facility, Covenant


fp = os.path.dirname(os.path.realpath(__file__))


def driver(args):
    assignments = get_loan_assignments(args)
    save_yields(assignments)
    save_assignments(assignments)

def save_assignments(assignments):
    with open(fp + '/data/assignments.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['loan_id', 'facility'])
        writer.writeheader()
        for assignment in assignments:
            writer.writerow({
                'loan_id': assignment['loan_id'],
                'facility': assignment['facility'].id
            })

def save_yields(assignments):
    facilities = set([assignment['facility'] for assignment in assignments])
    with open(fp + '/data/yields.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile,
            fieldnames=['facility_id', 'expected_yield'])
        writer.writeheader()
        for facility in facilities:
            writer.writerow({
                'facility_id': facility.id,
                'expected_yield': int(round(facility.expected_yield))
            })

def get_loan_assignments(args):
    facilities = get_facilities(args.facilities)
    covenants = get_covenants(args.covenants)
    csvreader = csv.reader(open(fp + args.loans))
    headers = next(csvreader, None)
    assignments = []
    for row in csvreader:
        loan = Loan(dict(zip(headers, row)))
        idx = 0  # start with facility with the lowest interest rate
        while idx < len(facilities):
            facility = facilities[idx]
            covenant_id = '{}.{}'.format(facility.id, loan.state)
            if facility.has_amount(loan):
                if covenants.get(covenant_id):
                    covenant = covenants[covenant_id]
                    if (covenant.banned_facility_id(facility) or
                        covenant.above_default(loan) or
                        covenant.banned_state(loan)):
                        idx += 1
                        continue
                facility.calculate_amount_remaining(loan)
                facility.calculate_expected_yield(loan)
                assignments.append({
                    'loan_id': loan.id,
                    'facility': facility
                })
                idx = 0  # start again with 0th facility
                break
            else:
                if facility.amount == 0:
                    facilities.remove(facility)
                idx += 1
    return assignments


def get_covenants(filename):
    with open(fp + filename) as infile:
        dictreader = csv.DictReader(infile)
        covenants = {'{}.{}'.format(row['facility_id'],
            row['banned_state']): Covenant(row) for row in dictreader}
        return covenants


def get_facilities(filename):
    with open(fp + filename) as infile:
        dictreader = csv.DictReader(infile)
        facilities = [Facility(row) for row in dictreader]
        facilities.sort(key=lambda f: float(f.interest_rate))  # sort by interest rate
        return facilities
