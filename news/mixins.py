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