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
							self.author.append(author[i][0])
						self.found_author = 1
		""" The condition, where we know if we need to parse another page
			"""
		if(self.found_author==1):
			print('There is an author')
		else:
			print('Author not found')

	def find_year (self, fpt):
                regex = r"(?:19[7-9]\d|2\d{3})(?=\D|$)"
                with open (fpt) as f:
                        for line in f:
                                        year = re.findall (regex, line)
                                        if year:
                                                for name in year:
                                                        self.year.append(name)
                                                self.found_year = 1

                if (self.found_year == 1):
                        print ('There is a year')
                else:
                        print ('Year not found')
                                        
		f.close()
					
