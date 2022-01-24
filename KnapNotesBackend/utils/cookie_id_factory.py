from secrets import token_hex
import numpy as np

SITE_IDENTIFIER = "KnapNotes"
TOKEN_RANDOM_PART_SIZE = 20


class UniqueTidbitProvider:

	def __init__(self):
		self.MIN_VALUE = np.iinfo(np.uint64).min
		self.MAX_VALUE = np.iinfo(np.uint64).max
		self.unique_tidbit = self.MIN_VALUE

	def get_unique_tidbit(self):
		outcome = self.unique_tidbit
		self.unique_tidbit = self.unique_tidbit + 1 if self.unique_tidbit < self.MAX_VALUE else self.MIN_VALUE
		return str(outcome) + SITE_IDENTIFIER


UNIQUE_TIDBIT_PROVIDER = UniqueTidbitProvider()


def generate_token():
	return UNIQUE_TIDBIT_PROVIDER.get_unique_tidbit() + token_hex(TOKEN_RANDOM_PART_SIZE)
