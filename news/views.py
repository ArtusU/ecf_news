from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render, reverse
from django.views import generic
from .forms import CustomUserCreationForm, CategoryForm, PostForm
from .models import Category,Post
from .mixins import ValidExecutiveMixin, ValidWriterMixin


def home(request):
    return render(request, 'index.html')


class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'


class CategoryCreateView(LoginRequiredMixin, ValidExecutiveMixin, generic.CreateView):
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


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, ValidWriterMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def get_success_url(self):
        return reverse('news:category-list')

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs.update({
            "user_id": self.request.user.id
        })
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        post.writer = self.request.user
        post.save()
        return super(PostCreateView, self).form_valid(form)
