from django.urls import path
from .views import home, SignupView

app_name = 'news'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignupView.as_view(), name='signup')
]
