from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
STATUS_CHOICES = (
	('draft','Draft'),
	('published', 'Published'),
)


class Category(models.Model):
	title = models.CharField(max_length=100, verbose_name='Title')
	slug  = models.SlugField(max_length=150, unique=True)

	class Meta:
		verbose_name='Category'
		verbose_name_plural = 'Categories'

	
	def get_absolute_url(self):
		return reverse('categories', args=[self.slug])

		
	def __str__(self):
		return self.title


class Tag(models.Model):
	title = models.CharField(max_length=50, verbose_name='Tag')
	slug = models.SlugField(max_length=100, unique=True)

	class Meta:
		verbose_name='Tag'
		verbose_name_plural = 'Tags'


	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])
		

	def __str__(self):
		return self.title


class Post(models.Model):
	title = models.CharField(max_length=255, verbose_name='Title')
	slug = models.SlugField(unique=True)
	status = models.CharField(choices=STATUS_CHOICES, default='draft', max_length=10, verbose_name='Status')
	publication_date = models.DateTimeField(verbose_name='Created')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
	picture = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True, verbose_name='Picture')
	content = RichTextUploadingField(verbose_name='Content')
	author = models.CharField(max_length=30, default='Anonymous', verbose_name='Created by')
	tags = models.ManyToManyField(Tag)

	class Meta:
		verbose_name='Post'
		verbose_name_plural = 'Posts'

	def get_absolute_url(self):
		return reverse('articledetails', args=[self.slug])
		
	def __str__(self):
		return self.title

class Contact(models.Model):
	name = models.CharField(max_length=150, verbose_name='Name')
	email = models.EmailField()
	message_date = models.DateField()
	message = models.TextField(max_length=3000)

	def __str__(self):
		return self.name + self.email
		
