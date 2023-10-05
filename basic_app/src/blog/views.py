from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm

#GET implies that there is one object
#Filter implies that there was a list of objects

# CRUD

# GET -> Retrieve / List

# POST -> Create/ Update/ Delete

# CRUD is Create Read Update and Delete

def blog_post_list_view(request):
	# list out objects
	# could be search using filter instead of all
	qs=BlogPost.objects.all().published() # queryset -> list of objects
	if request.user.is_authenticated:
		my_qs=BlogPost.objects.filter(user=request.user)
		qs= (qs | my_qs).distinct()

	template_name='blog/list.html'
	context={'object_list': qs}
	return render(request,template_name,context)

# @login_required
@staff_member_required
def blog_post_create_view(request):
	# create objects
	# ?  use a form
	# now request.user will return something due to the decorator
	form=BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj=form.save(commit=False) # not actually saving data
		# you can make changes here
		obj.user=request.user
		obj.title=form.cleaned_data.get("title")
		obj.save()

		form=BlogPostModelForm()
	template_name='form.html'
	context={'form': form}
	return render(request,template_name,context)

def blog_post_detail_view(request,slug):
	# 1 object or the detail view
	obj=get_object_or_404(BlogPost, slug=slug)
	template_name='blog/detail.html'
	context={"object": obj}
	return render(request,template_name,context)

@staff_member_required
def blog_post_update_view(request,slug):
	obj=get_object_or_404(BlogPost, slug=slug)
	form=BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name='form.html'
	context={ 'form': form, "title": f"Update {obj.title}"}
	return render(request,template_name,context)

@staff_member_required
def blog_post_delete_view(request,slug):
	obj=get_object_or_404(BlogPost, slug=slug)
	template_name='blog/delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context={"object": obj}
	return render(request,template_name,context)
