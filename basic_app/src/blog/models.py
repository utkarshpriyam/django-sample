from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.

User=settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now=timezone.now()
		# here query set refers to blogpost.objects
		return self.filter(publish_date__lte=now)

	def search(self,query):
		lookup=(
					Q(title__icontains=query) | 
					Q(content__icontains=query) | 
					Q(slug__icontains=query) |
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
				)
		return self.filter(lookup)


# our own model manager to decide what data from model is to be shown

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model,using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)

# Allows us to store data in database in a very specific way

class BlogPost(models.Model):
	# id=models.IntegerField() # pk
	user=models.ForeignKey(User, null=True, default=1, on_delete=models.SET_NULL)
	image=models.ImageField(upload_to='image/', blank=True, null=True)
	title = models.CharField(max_length=120)
	# in url space is replaced by %20 slugs transform like a b->a-b
	slug = models.SlugField(unique=True) # url encoded value for lookup in the address bar
	content = models.TextField(null=True, blank=True)
	publish_date=models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	objects=BlogPostManager()

	class Meta:
		ordering = ['-publish_date','-updated','-timestamp']

	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_edit_url(self):
		return f"/blog/{self.slug}/edit"

	def get_delete_url(self):
		return f"/blog/{self.slug}/delete"





