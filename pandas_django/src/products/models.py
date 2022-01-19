from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Purchese(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quentity = models.PositiveIntegerField()
    total_price = models.PositiveSmallIntegerField(blank=True)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    #TODO:  change required
    date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quentity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Solled {self.product.name} - {self.quentity} items for {self.total_price}"
    
    