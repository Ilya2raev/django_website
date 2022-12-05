from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title':'О сайте', 'url_name': 'about'},
		{'title':'Добавить контент', 'url_name': 'add_content'},
		{'title':'Обратная связь', 'url_name': 'feedback'},
]

class DataMixin:
	paginate_by = 3

	def get_user_context(self, **kwargs):
		context = kwargs
		categories = cache.get('categories')
		if not categories:
			categories = Category.objects.annotate(Count('cats'))
			cache.set('categories', categories, 60)

		user_menu = menu.copy()
		if not self.request.user.is_authenticated:
			user_menu.pop(1)

		context['menu'] = user_menu

		context['categories'] = categories
		if 'category_selected' not in context:
			context['category_selected'] = 0
		return context 