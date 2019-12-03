from django.db import models
from django_enumfield import enum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserType(enum.Enum):
    NONE = 0
    FREE = 1
    PAID1 = 2
    PAID2 = 3
    PAID3 = 4
    
class UniType(enum.Enum):
    NONE = 0
    SURFACE_TRACKING = 1
    IMAGE_TARGET = 2

class UniFileType(enum.Enum):
    NONE = 0
    AUDIO = 1
    VIDEO = 2
    MODEL = 3

class UniCategory(enum.Enum):
    NONE = 0
    ENTERTAINMENT = 1
    SCIENCE = 2
    ART = 3
    INDUSTRIAL = 4
    COMERCE  = 5
    
class LoginType(enum.Enum):
    NONE = 0
    FACEBOOK = 1
    EMAIL = 2

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fbid = models.TextField(max_length=500, blank=True, null = True)
    followers = models.IntegerField(null=True, blank=True)
    following = models.IntegerField(null=True, blank=True)
    unisAmount = models.IntegerField(null=True, blank=True)
    imageBytes = models.BinaryField(null=True, blank=True)
    image = models.FileField(upload_to='ProfileImages/', null=True, blank=True)
    userType = enum.EnumField(UserType, default=UserType.FREE)
    loginType = enum.EnumField(LoginType, default=LoginType.EMAIL)
    followers_user = models.ManyToManyField('self', related_name='follows', symmetrical=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UniAR(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    uniCategory = enum.EnumField(UniCategory, default=UniCategory.ENTERTAINMENT)
    imageBytes = models.BinaryField(null=True, blank=True)
    fileBytes = models.BinaryField(null=True, blank=True)
    uniType  = enum.EnumField(UniType, default=UniType.IMAGE_TARGET)
    uniFileType = enum.EnumField(UniFileType, default=UniFileType.MODEL)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    uniHyperLink = models.CharField(max_length=300, null=True, blank=True)
    fileSize = models.IntegerField(null=True, blank=True)
    isPrivate = models.BooleanField(null=True, blank=True)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    position_z = models.FloatField(null=True, blank=True)
    rotation_x = models.FloatField(null=True, blank=True)
    rotation_y = models.FloatField(null=True, blank=True)
    rotation_z = models.FloatField(null=True, blank=True)
    scale_x = models.FloatField(null=True, blank=True)
    scale_y = models.FloatField(null=True, blank=True)
    scale_z = models.FloatField(null=True, blank=True)
    
    
 