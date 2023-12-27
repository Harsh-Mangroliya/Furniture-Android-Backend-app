from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('users.user', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.customer.username
    
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField( max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.customer.username

class Cart(models.Model):
    customer = models.ForeignKey('users.user', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.customer.username