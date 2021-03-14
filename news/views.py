from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.views import generic
from .forms import CustomUserCreationForm, CategoryForm
from .models import Category


def home(request):
    return render(request, 'index.html')


class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_create.html'
    
    def get_success_url(self):
        return reverse('news:category-list')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.executive = self.request.user
        category.save()
        return super(CategoryCreateView, self).form_valid(form)