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
		self.author_line = 0
		self.title = ''
		self.doi = None

	def find_author(self, fpt):
		i = 0
		num = 0
		regex = r"((([A-Z][a-z]+)|([A-Z]\.))\s+(([A-Z]\.)|([A-Z][a-z]+))\s*(([A-Z][a-z]+)|(\,)))"
		with open(fpt) as f:
    			for line in f:
					author = re.findall(regex, line)
					num = num + 1
					if author:
						if self.author_line == 0:
							self.author_line = num-1
						for i in range(0, len(author)):
							if(len(self.author)==0):
								self.author.append(author[i][0])
							elif(self.author[len(self.author)-1]!=author[i][0]):
								self.author.append(author[i][0])
						self.found_author = 1
		""" The condition, where we know if we need to parse another page
			
		if(self.found_author==1):
			print('There is an author')
		else:
			print('Author not found')
			"""
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

	def find_title (self, fpt):
			i = 0
			title = [None] * 3
			with open (fpt) as f:
				for line in f: 
					if(len(line)>1):
						title[(i)%3] = line	
					i+=1
					if i == self.author_line:
						break
			for i in range (i-1, i+2):
				if(title[i%3]):
					self.title += title[i%3]
			
			f.close()	

	def find_doi (self, fpt):

		regex = r"(doi.*)"
		with open (fpt) as f:
			for line in f:
				doi = re.search (regex, line, re.IGNORECASE)
				if doi:
					self.doi = doi.group(0)
					break            
		f.close()
