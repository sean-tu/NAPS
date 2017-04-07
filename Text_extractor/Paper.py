""" class "paper" with metadata and the reference to the text of the paper.
	Still needs to be worked on
	"""
class Paper:

	def __init__(self):
		self.num_pages = 0
		self.author = None
		self.doi = None
		self.title = 'TITLE'
		self.text = None
		self.year = 0
		self.publisher = 'PUBLISHER'
		self.pages_range = None

	def set_pages(self,pages):
		self.num_pages = pages

	def set_doi(self, doi):
		self.doi = doi

	def get_pages(self):
		return self.num_pages
	
	def set_author(self, name):
		self.author = name

	def set_title(self, title):
		self.title = title

	def set_year (self, year):
		self.year = year

	def set_doi(self, doi):
		self.doi = doi

	def set_text(self, fpt):
		self.text = fpt

	def set_publisher(self, name):
		self.publisher = name

	def set_page_range(self, nums):
		self.pages_range = nums

	""" Debugging to see if it works
		"""
	def generate_citations(self, fpt):
		fp = file(fpt, 'w')
		fp.write('Author:')
		for author in self.author:
			if(author.endswith(',')):
				fp.write(str(author) + ' ');
			else:
				fp.write(str(author) + ', ');
		fp.write('\nTitle : ' + self.title + ' ')
		fp.write('\nPublisher : ' + self.publisher + ' ')
		fp.write('\nYear of publication : ' + str(self.year) + ' ')
		fp.write('\nPages in the journal : ' + str(self.pages_range) + ' ')
		fp.write('\n' + self.doi)
		fp.close()
