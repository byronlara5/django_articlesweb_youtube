from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator


from post.models import Post, Category, Tag, Contact
from django.db.models import Q

from post.forms import ContactForm
from django.utils import timezone

# Create your views here.

def index(request):
	articles = Post.objects.filter(status='published').order_by('-publication_date')
	categories = Category.objects.all()

	#Search
	query = request.GET.get("q")

	if query:
		articles = articles.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)).distinct()


	#Pagination
	paginator = Paginator(articles, 6)
	page_number = request.GET.get('page')
	articles_paginator = paginator.get_page(page_number)


	template = loader.get_template('index.html')

	context = {
		'articles': articles_paginator,
		'categories': categories,
	}

	return HttpResponse(template.render(context, request))


def category(request, category_slug):
	articles = Post.objects.filter(status='published').order_by('-publication_date')
	categories = Category.objects.all()

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		articles = articles.filter(category=category)

	#Complete your homework here

	template = loader.get_template('category.html')

	context = {
		'articles':articles,
		'categories':categories,
	}

	return HttpResponse(template.render(context, request))


def tags(request, tag_slug):
	tags = Tag.objects.all()
	articles = Post.objects.filter(status='published').order_by('-publication_date')

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		articles = articles.filter(tags=tag)

	#Complete your homework here

	template = loader.get_template('tags.html')

	context = {
		'articles':articles,
	}

	return HttpResponse(template.render(context, request))

def PostDetails(request, post_slug):
	article = get_object_or_404(Post, slug=post_slug)

	template = loader.get_template('post_detail.html')

	context = {
		'article':article,
	}

	return HttpResponse(template.render(context, request))


def Contact(request):
	
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.message_date = timezone.now()
			form.save()
			return redirect('contactsuccess')
	else:
		form = ContactForm()

	context = {
		'form':form,
	}

	return render(request, 'contact.html', context)


#static website for the form contact

def ContactSuccess(request):
	return render(request, 'contactsuccess.html',)




