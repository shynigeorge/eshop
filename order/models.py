from django.contrib.auth.models import User
from django.db import models

from homepage.models import Product


class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    fname =models.CharField(max_length=250, null=False)
    lname = models.CharField(max_length=250, null=False)
    email = models.EmailField(max_length=250, null=False)
    mobileno = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250, null=False)
    country = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    state = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=250, null=False)

    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=250, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatus =(
        ('Pending','Pending'),
        ('Out of Shipping', 'Out of Shipping'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=250, choices=orderstatus,default='Pending')
    message = models.TextField(null=True)
    tracking_no= models.CharField(max_length=250, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.id,self.tracking_no)

class Itemorder(models.Model):
    ord = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.ord.id, self.ord.tracking_no)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileno = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250, null=False)
    country = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    state = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=250, null=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




