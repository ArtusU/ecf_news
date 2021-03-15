from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email           = models.EmailField(unique=True, max_length=255)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_type       = models.CharField(max_length=100, choices=(
                                                                ("Executive", "Executive"),
                                                                ("Manager", "Manager"),
                                                                ("Writer", "Writer"),
                                                                ("Reader", "Reader"),
                                                                ), default='Reader')

    def __str__(self):
        return self.user.email


class Category(models.Model):
    executive       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    managers        = models.ManyToManyField(CustomUser, related_name='managers_category')
    writers         = models.ManyToManyField(CustomUser, related_name='writers_category')

    name            = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    writer          = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)

    title           = models.CharField(max_length=100)
    content         = models.CharField(max_length=255)
    date_created    = models.DateTimeField(auto_now_add=True)
    last_updated    = models.DateTimeField(auto_now=True)
    public          = models.BooleanField(default=False)

    def __srt__(self):
        return self.title





class Subscription(models.Model):
    reader          = models.ForeignKey(CustomUser, related_name='user_subscriptions', on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, related_name='category_subscriptions', on_delete=models.CASCADE)

    def __str__(self):
        return self.reader.email







def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_save_user_receiver, sender=CustomUser)