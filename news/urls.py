from django.urls import path
from .views import CategoryListView, home, SignupView, CategoryCreateView, CategoryDetailView, PostDetailView, PostCreateView

app_name = 'news'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('category/', CategoryListView.as_view(), name='category-list'),
    path('categories/<pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),

    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', PostCreateView.as_view(), name='post-create')
]
