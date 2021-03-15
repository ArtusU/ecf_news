from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views import generic
from .forms import CustomUserCreationForm, CategoryForm, PostForm, SubscribeCategoryForm
from .models import Category, Post, Subscription
from .mixins import ValidExecutiveMixin, ValidWriterMixin, ValidMangerMixin, ManagerHasAccessMixin


def home(request):
    return render(request, 'index.html')


class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryDetailView(generic.FormView):
    form_class = SubscribeCategoryForm
    template_name = 'category_detail.html'

    def get_success_url(self):
        return reverse('news:category-detail', kwargs={
            'pk': self.kwargs['pk']
        })

    def form_valid(self, form):
        if not self.request.user.userprofile.user_type == 'Reader':
            return redirect(reverse('news:category-detail', kwargs={
            'pk': self.kwargs['pk']
            }))
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        Subscription.objects.get_or_create(
            reader=self.request.user,
            category=category
        )
        return super(CategoryDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['subscribed'] = False
        try:
            Subscription.objects.get(
                reader=self.request.user,
                category=category
            )
            context['subscribed'] = True
        except Subscription.DoesNotExist:
            pass
        context.update({
            'category': category
        })
        return context


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
        return reverse("news:category-list")

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

class PostDeleteView(generic.DetailView):
    model = Post
    success_url = '/category'
    template_name = 'post_confirm_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(writer=user.organization)


class ManagerPostListView(LoginRequiredMixin, ValidMangerMixin, generic.ListView):
    template_name = 'manager_post_list.html'

    def get_queryset(self):
        categories = list(self.request.user.managers_category.values_list('id', flat=True))
        qs = Post.objects.filter(category__id__in=categories)
        return qs


class ManagerMarkAsPublic(LoginRequiredMixin, ValidMangerMixin, ManagerHasAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['pk'])
        post.public = True
        post.save()
        return redirect(reverse("news:post-detail", kwargs={'pk': kwargs['pk']}))


class CategoryFeedView(LoginRequiredMixin, generic.ListView):
    template_name = 'feed.html'

    def get_queryset(self):
        #return Subscription.objects.filter(reader=self.request.user)
        return self.request.user.user_subscriptions.all()