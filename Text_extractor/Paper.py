""" class "paper" with metadata and the reference to the text of the paper.
	Still needs to be worked on
	"""
class Paper:

	def __init__(self):
		self.num_pages = 0
		self.author = ''
		self.doi = None
		self.title = 'TITLE'
		self.year = 0
		self.publisher = 'PUBLISHER'
		self.pages_range = None

	def set_pages(self,pages):
		self.num_pages = pages

	def set_doi(self, doi):
		self.doi = doi
	
	def set_author(self, name):
		for author in name:
			if(author.endswith(',')):
				self.author += (str(author) + ' ');
			else:
				self.author += (str(author) + ', ');

	def set_title(self, title):
		self.title = title

	def set_year (self, year):
		self.year = year

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

		fp.write('\nTitle : ' + self.title + ' ')
		fp.write('\nPublisher : ' + self.publisher + ' ')
		fp.write('\nYear of publication : ' + str(self.year) + ' ')
		fp.write('\nPages in the journal : ' + str(self.pages_range) + ' ')
		fp.write('\n' + self.doi)
		fp.close()


	def get_doi(self):
		return str(self.doi)
	
	def get_author(self):
		return str(self.author)

	def get_title(self):
		return str(self.title)

	def get_year (self):
		return str(self.year)

	def get_publisher(self):
		return str(self.publisher)

	def get_page_range(self):
		return str(self.pages_range)

	def get_pages(self):
		return self.num_pages
