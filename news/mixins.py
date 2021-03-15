from news.models import Post
from django.core.exceptions import PermissionDenied


class ValidExecutiveMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.userprofile.user_type != 'Executive':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ValidWriterMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.userprofile.user_type != 'Writer':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ValidMangerMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.userprofile.user_type != 'Manager':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ManagerHasAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['pk'])
        if request.user in post.category.managers.all():
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied