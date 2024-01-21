from django.db import models

class Order(models.Model):
    modeOfPaymentChoices = (
        ('COD','Cash On Delivery'),
        ('ONLINE','Online Payment'),
    )

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('users.user', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    modeOfPayment = models.CharField(max_length=10, choices=modeOfPaymentChoices, default='COD')
    cardDetailId = models.ForeignKey('users.CardDetail', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.customer.username
    
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField( max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.order.customer.username

