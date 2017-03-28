"""Class matadata - the only purpose is to search for an author/title etc.
	if nothing found, returns a flag, which means that the page is probably wrong, so
	the other page needs to be parsed.
	Still not finished
	"""
import re

class Metadata:

	def __init__(self):
		self.found_author = 0
		self.found_title = 0
		self.author = []

	def find_author(self, fpt):
		regex = r"([A-Z][a-z]+\s+[A-Z][a-z]+)"
		with open(fpt) as f:
    			for line in f:
					author = re.findall(regex, line)
					if author:
						for name in author:
							self.author.append(name)
						self.found_author = 1

		""" The condition, where we know if we need to parse another page
			"""
		if(self.found_author==1):
			print('There is an author')
		else:
			print('Author not found')
		f.close()
					