from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class productImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImage')

    def __str__(self):
        return self.product.name
    
    def image_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.image)
