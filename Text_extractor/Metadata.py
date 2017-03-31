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
		self.pages = 0
		self.year = []
		self.found_doi = 0
		self.found_year = 0
		self.author = []

	def find_author(self, fpt):
		i = 0
		regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))\s*(([A-Z][a-z]+)|(\,)))"
		with open(fpt) as f:
    			for line in f:
					author = re.findall(regex, line)
					if author:
						for i in range(0, len(author)):
							if(len(self.author)==0):
								self.author.append(author[i][0])
							elif(self.author[len(self.author)-1]!=author[i][0]):
								self.author.append(author[i][0])
						self.found_author = 1
		""" The condition, where we know if we need to parse another page
			"""
		if(self.found_author==1):
			print('There is an author')
		else:
			print('Author not found')
		f.close()

	def find_year (self, fpt):
		regex = r"(?:19[7-9]\d|2\d{3})(?=\D|$)"
		with open (fpt) as f:
			for line in f:
				year = re.search (regex, line)
				if year:
					self.year = year.group(0)
                                        
		f.close()

	def find_range (self, fpt):
		regex = r"([0-9]+-[0-9]+)"
		with open (fpt) as f:
			for line in f:
				pages = re.search (regex, line)
				if pages:
					self.pages = pages.group(0)
					break             
		f.close()

					
