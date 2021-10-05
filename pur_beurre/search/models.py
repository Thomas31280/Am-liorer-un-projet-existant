from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    
    category = models.CharField(max_length=100, unique=True)              # On met évidement une contrainte d'unicité sur les catégories

    def __str__(self):                                                    # On définit un l'attribut à afficher pour la QuerySet
        return self.category

class Aliment(models.Model):
    
    pnns_groups_1 = models.ForeignKey(Category, on_delete=models.CASCADE) # On s'assure que la supression d'une catégorie dans la table Category entrainera également la supression des tous les aliments qui appartiennent à cette catégorie.
    product_name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(unique=True)                                    # Unique=True to be sure to not introduce a product more than 1 time
    img_url = models.URLField(default=None)

    def __str__(self):
        return self.product_name

class Favorites(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Aliment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_id', 'product_id'),)                    # On pose une contrainte d'unicité composite sur les deux champs spécifiés

    def __str__(self):
        return self.product_id
