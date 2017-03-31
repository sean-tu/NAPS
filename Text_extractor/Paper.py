""" class "paper" with metadata and the reference to the text of the paper.
	Still needs to be worked on
	"""
class Paper:

	def __init__(self):
		self.num_pages = 0
		self.author = None
		self.title = None
		self.text = None
		self.year = 0

	def set_pages(self,pages):
		self.num_pages = pages

	def get_pages(self):
		return self.num_pages
	
	def set_author(self, name):
		self.author = name

	def set_title(self, title):
		self.title = name

	def set_year (self, year):
                self.year = year

	def set_doi(self, doi):
                self.doi = doi

	def set_text(self, fpt):
		self.text = fpt

	""" Debugging to see if it works
		"""
	def printinfo(self, fpt):
		fp = file(fpt, 'w')
		fp.write('num pages = ' + str(self.num_pages)+'\n')
		fp.write('author = '+str(self.author)+'\n')
		fp.write('title = '+str(self.title)+'\n')
		fp.write('year = '+str(self.year)+'\n')
		fp.close()
