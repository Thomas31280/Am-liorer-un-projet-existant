from django.db import models

# Create your models here.

class Aliment(models.Model):
    
    pnns_groups_1 = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(unique=True)                               # Unique=True to be sure to not introduce a product more than 1 time

class User(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    aliments = models.ManyToManyField(Aliment, related_name="favorites")
