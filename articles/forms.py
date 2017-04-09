import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Article

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		exclude = ['pdf_file','full_text','features']

def clean_file_ext(file):
	names = file.name.split('.')
	if names[-1] != 'pdf':
		raise ValidationError(
            ('Only .pdf files are allowed!'),
        )

class PartialArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['pdf_file',]

	pdf_file = forms.FileField( #=forms.FileField
		label='Select a PDF',
		help_text='upload a .pdf file from your local files',
		validators=[clean_file_ext]
    )