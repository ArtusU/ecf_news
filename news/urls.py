from django.urls import path
from .views import CategoryListView, home, SignupView, CategoryCreateView

app_name = 'news'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create')
]
