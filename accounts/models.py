from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, null=True, on_delete=CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    document_type = models.CharField(max_length=20, null=True)
    document = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    image = models.ImageField(default="profile.png", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door')
    )

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=5, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS=(
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, choices=STATUS)
    note = models.CharField(max_length=300, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)