from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound	
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *

class CatsHome(DataMixin, ListView):
	model = Cats
	template_name = 'cats/index.html'
	context_object_name = 'posts'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Главная страница')
		return dict(list(context.items()) + list(c_def.items()))

	def get_queryset(self):
		return Cats.objects.filter(is_published=True)

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddContentForm
	template_name = 'cats/addcontent.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')
	raise_exception = True

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Добавить контент')
		return dict(list(context.items()) + list(c_def.items()))

class ContactFormView(DataMixin, FormView):
	form_class = ContactForm
	template_name = 'cats/contact.html'
	success_url = reverse_lazy('/')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Обратная связь')
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):
		print(form.cleaned_data)
		return redirect('/')

def about(request):
	return render(request, 'cats/about.html', {'menu': menu, 'title': 'О сайте'})

class ShowPost(DataMixin, DetailView):
	model = Cats
	template_name = 'cats/post.html'
	slug_url_kwarg = 'post_slug'
	context_object_name = 'post'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title=context['post'])
		return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Ошибка 404</h1>')

class CatsCategory(DataMixin, ListView):
	model = Cats
	template_name = 'cats/index.html'
	context_object_name = 'posts'
	allow_empty = False

	def get_queryset(self):
		return Cats.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title=str(context['posts'][0].category),
			category_selected=context['posts'][0].category_id)
		return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
	form_class = RegisterUserForm
	template_name = 'cats/register.html'
	success_url = reverse_lazy('login')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Регистрация')
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('/')

class LoginUser(DataMixin, LoginView):
	form_class = LoginUserForm
	template_name = 'cats/login.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title='Авторизация')
		return dict(list(context.items()) + list(c_def.items()))

def logout_user(request):
	logout(request)
	return redirect('/')
