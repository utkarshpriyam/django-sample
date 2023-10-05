from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .form import ContactForm
from blog.models import BlogPost
# Dont repeat yourself

def home_page(request):
	qs=BlogPost.objects.all()[:5]
	context={"title": "Welcome to try django", "blog_list": qs}
	return render(request, "home.html", context)

def about_page(request):
	return render(request, "about.html", {"title": "About us"})

def contact_page(request):
	form=ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form=ContactForm()
	context={
		"title": "Contact us",
		"form": form
	}
	return render(request, "form.html", context)

def example_page(request):
	context = {"title": "Example"}
	template_name = "hello_world.html"
	template_obj=get_template(template_name)
	return HttpResponse(template_obj.render(context))