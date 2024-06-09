from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.forms import ValidationError

from accounts.manager import CustomUserManager

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


@receiver(pre_save, sender=User)
def set_username_from_email(sender, instance, **kwargs):
    if instance._state.adding :
        instance.username = instance.email.split('@')[0]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', symmetrical=False, through='Friendship')

    def __str__(self) -> str:
        return self.user.username


class Friendship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='to_user', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("A user cannot add themselves as a friend.")

    class Meta:
        unique_together = ['from_user','to_user']

    def __str__(self) -> str:
        return self.from_user.user.email +' - '+ self.to_user.user.email

