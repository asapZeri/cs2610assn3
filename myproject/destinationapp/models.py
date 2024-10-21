from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

class Destination(models.Model):
    name = models.TextField()
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_publicly = models.BooleanField(default=False)