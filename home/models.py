from django.db import models

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=122,null=True)
    email = models.CharField(max_length=122,null=True)
    phone_no = models.CharField(max_length=122,null=True)
    password = models.CharField(max_length=200,null=True)
    store_name = models.CharField(max_length=16,null=True)
    status = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.store_id} {self.name}'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=122,null=True)
    email = models.CharField(max_length=122,null=True)
    phone_no = models.CharField(max_length=122,null=True)
    password = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=16,null=True)
    status = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.user_id} {self.email}'




class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=122,null=True)
    store_id = models.ForeignKey(Store,on_delete=models.CASCADE,null=True,related_name="store")
    product_image = models.FileField(upload_to='',default='')
    price = models.FloatField(default=0.0)
    description = models.CharField(max_length=800,null=True)
    quantity = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.product_id} {self.product_name}'


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="User")
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True, related_name="Product")
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    status = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)