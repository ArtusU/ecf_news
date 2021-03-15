from django.urls import path
from .views import CategoryListView, home, SignupView, CategoryCreateView, CategoryDetailView, PostDetailView, PostCreateView, PostDeleteView, ManagerPostListView, ManagerMarkAsPublic, CategoryFeedView

app_name = 'news'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('feed/', CategoryFeedView.as_view(), name='feed'),

    path('category/', CategoryListView.as_view(), name='category-list'),
    path('categories/<pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),

    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('manager/posts/', ManagerPostListView.as_view(), name='manager-post-list'),
    path('manager/posts/<pk>/mark-as-public', ManagerMarkAsPublic.as_view(), name='mark-as-public')
]
