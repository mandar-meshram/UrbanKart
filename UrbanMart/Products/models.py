from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Categories.Category', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    








    # CASCADE means if the category is deleted, all products in that category will also be deleted.and applies only on foreign key fields. 
    # CASCADE is a type of referential action that specifies what should happen to the related objects when the referenced object is deleted.