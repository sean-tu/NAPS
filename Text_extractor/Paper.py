""" class "paper" with metadata and the reference to the text of the paper.
	Still needs to be worked on
	"""
class Paper:

	def __init__(self):
		self.num_pages = 0
		self.author = None
		self.title = None
		self.text = None

	def set_pages(self,pages):
		self.num_pages = pages
	
	def set_author(self, name):
		self.author = name

	def set_title(self, title):
		self.title = name

	def set_doi(self, doi):
                self.doi = doi

	def set_text(self, fpt):
		self.text = fpt

	""" Debugging to see if it works
		"""
	def printinfo(self):
		print('num pages = ' + str(self.num_pages)+'')
		print('author = '+str(self.author))
		print('title = '+str(self.title))
