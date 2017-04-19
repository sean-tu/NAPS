#import Django's template rendering
from django.shortcuts import render, get_object_or_404, redirect
#import django's login_required decorator
from django.contrib.auth.decorators import login_required
#import the singup form
from django.contrib.auth.forms import UserCreationForm
#import the Article model
from .models import Article # the . means same directory and eliminates need for .py extension
#import the Articles forms from forms.py
from .forms import ArticleForm, PartialArticleForm
#import the file type checker
#from .utilities import ExtFileField

# Create your views here.

#article_list: lists all of a user's articles.
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'registration/signup_success.html', {'form': form})
		else:
			return render(request, 'registration/signup.html', {'form': form})
	else:
		form = UserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})

@login_required
def article_list(request):
	current_user = request.user
	articles = Article.objects.filter(owner = current_user).order_by('category')
	return render(request, 'articles/article_list.html', {'articles':articles, 'categories':Article.CATEGORIES})

#article_update: updates an Article instance on POST request, serves a form on GET or other request
@login_required
def article_update(request, pk):
	article = get_object_or_404(Article, pk=pk)
	if request.method == 'POST':
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			#does this return the same object?
			form.save()
			return render(request, 'articles/article_detail.html', {'article' : article, 'message':'Article updated!', 'message_type':'success'})
		else:
			return render(request, 'articles/article_update.html', {'form':form, 'article':article, 'message': 'Sorry, there was a problem with the information you entered.'})
	else:
		form = ArticleForm(instance=article)
		for field in form:
			field.css_classes('form-control')
		return render(request, 'articles/article_update.html', {'form':form, 'article':article})

#detail: displays the details of a single Article
@login_required
def article_detail(request, pk):
	article = get_object_or_404(Article, pk=pk)
	return render(request, 'articles/article_detail.html', {'article' : article})

#delete: removes an article record
@login_required
def article_delete(request, pk):
	current_user = request.user
	article = get_object_or_404(Article, pk=pk)
	if article.owner == current_user:
		article.delete()
		articles = Article.objects.filter(owner = current_user).order_by('category')
		return render(request, 'articles/article_list.html', {'articles':articles, 'categories':Article.CATEGORIES, 'message':'Article successfully deleted.', 'message_type':'success'})
	else:
		articles = Article.objects.filter(owner = current_user).order_by('category')
		return render(request, 'articles/article_list.html', {'articles':articles, 'categories':Article.CATEGORIES, 'message':'You cant\'t delete an article that isn\'t yours!'})


#upload_pdf: on a POST request, creates a new Article object belonging to current user with uploaded file,
#	and displays an upload form on GET or any other request
@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PartialArticleForm(request.POST, request.FILES)
        if form.is_valid():	
            #save file but not the Article yet
            article = form.save(commit=False)
            article.owner = request.user
            #create a new Extractor and pass article.file to it
            article.save()
            article.extract()
            article.save(update_fields=['full_text', 'doi', 'authors', 'date_published', 'publisher'])
            #create a new Classifier and pass article.file to it
            article.categorize()
            article.save(update_fields=['category', 'subcategory'])
            #if certainty is low:
            	#article.save
            	#redirect to a select category page
            #if certainty is high:
            	#set article category and save
            return redirect('article_detail', pk=article.pk)
        else:
        	return render(request, 'articles/pdf_upload.html', {'form': form, 'message':'There was a problem uploading your PDF file.'})
    else:
        form = PartialArticleForm()
    return render(request, 'articles/pdf_upload.html', {'form': form})

def home(request):
	return render(request, 'articles/home.html')

def about(request):
	return render(request, 'articles/about.html')