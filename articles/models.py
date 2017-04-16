from __future__ import unicode_literals
from django.db import models
from NAPS.settings import MEDIA_ROOT
import re
import datetime
import random

#import the Classifier class from /classify/classify.py
from classification import classification
#import the Extractor class from /extractor/extract.py
from Text_extractor import extract, get_info, Paper


# Create your models here.
class Article(models.Model):

	#list of Categories used by the Classifier
	category_list = ['Anthropology', 'Chemistry', 'Computer Science', 'Earth Science', 'Engineering', 'Life Science', 'Materials Science', 'Medicine', 'Mathematics', 'Physics']
	CATEGORIES = []
	for cat in category_list:
		CATEGORIES.append( (cat.lower().replace(' ','-'), cat) )

	# pk (primary key) will be created automagically when Article is saved
	#required fields: owner, pdf_file
	owner = models.ForeignKey('auth.User', editable=False)
	pdf_file = models.FileField(upload_to='uploaded-pdfs/')

	#fields to be extracted (can be blank in case of not able to extract)
	title = models.CharField(max_length=100, blank=True, null=True)
	authors = models.CharField(max_length=200, blank=True, null=True)
	publisher = models.CharField(max_length=100, blank=True, null=True)
	date_published = models.IntegerField(max_length=4, blank=True, null=True)
	doi = models.CharField(max_length=50, blank=True, null=True)
	features = models.TextField(blank=True, null=True)
	category = models.CharField(max_length=50, choices=CATEGORIES, blank=True, null=True)
	subcategory = models.CharField(max_length=50, blank=True, null=True)
	full_text = models.TextField(blank=True, null=True, editable=False)
	
	def __str__(self):
		return self.title + ' (' + self.authors + ')'

	def categorize(self):
		self.category = 'Chemistry'
		self.subcategory = 'Analytical Chemistry'
		#categories = classification.classify(self.full_text)
		#self.category = categories[0]
		#self.subcategory = categories[1]

	def extract(self):
		tmp_filename = MEDIA_ROOT + 'text-' + str( random.randint(100000,999999) ) + '.txt'
		extract.extract(self.pdf_file.url, tmp_filename)
		self.full_text = open(tmp_filename, 'r').read()
		paper = get_info.get_info(self.pdf_file.url, tmp_filename)
		self.doi = paper.get_doi()
		self.authors = paper.get_author()
		self.title = paper.get_title()
		self.date_published = paper.get_year()
		self.publisher = paper.get_publisher()


	def validate_category(self, input_category):
		if (input_category in Article.CATEGORIES):
			self.category = input_category
		else:
			self.category = ""

	def display_category(self):
		return self.category.replace('-',' ').title()

	def format_authors_mla(self):
		#use with flag re.U. Gets fullname, first, last but may match 0-9 or _, so be sure to strip those.
		names_pattern = '(?P<fullname>(?P<first>(\w((\.\s)|\w+\s))+)(?P<last>\w+))'
		name_iter = re.compile(names_pattern, re.U).finditer(self.authors)
		formatted_authors = ''
		for author in list(name_iter):
			formatted_authors += author.group('last').strip('[0-9_]') + ', ' + author.group('first').strip('[0-9_]') + ', '
		#remove the last comma & return
		return formatted_authors.strip(', ')

	def format_authors_apa(self):
		#use with flag re.U. Gets fullname, first, last but may match 0-9 or _, so be sure to strip those.
		names_pattern = '(?P<fullname>(?P<first>(\w((\.\s)|\w+\s))+)(?P<last>\w+))'
		name_iter = re.compile(names_pattern, re.U).finditer(self.authors)
		formatted_authors = ''
		for author in list(name_iter):
			#Must convert first name(s) to initials
			raw_first = author.group('first')
			#Split first name string by spaces
			first_names = re.split(' ', raw_first)
			formatted_first = ''
			for n in first_names:
				#drop junk words
				n = n.strip('[\s*]')
				if (n == 'and' or n == '&' or n== '' ):
					continue
				#if already an initial, add back to first name
				if ( re.match('\s*\w\.\s*', n) ):
					formatted_first += n
				#Otherwise truncate & add period
				else:
					formatted_first += n.strip('[0-9_]')[:1] + '. '
			formatted_authors += author.group('last') + ', ' + formatted_first + ', '
		#remove the last comma & return
		return formatted_authors.strip(', ')