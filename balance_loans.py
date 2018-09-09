import argparse
import sys
from loan_balance import driver


INFILES = ('facilities', 'banks', 'covenants', 'loans')
SUCCESS_MSG = ('\033[92mSuccess! Your loans are now balanced.\n' +
		  'Look in "/loan_balance/data/" for the "assignments" ' +
		  'and "yields" files. \033[0m \n')

def main(args):
	driver(args)
	sys.stdout.write(SUCCESS_MSG)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	for file in INFILES:
		parser.add_argument('--{}'.format(file),
							help='Path to a {} file'.format(file),
							default='/data/{}.csv'.format(file))
	args = parser.parse_args()
	main(args)
