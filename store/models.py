from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    present_address = models.CharField(max_length=200, blank=True)
    permanent_address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    old_card = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
#Create a user Profile by default when user Sing up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save

#Automate the profile thing
post_save.connect(create_profile, sender=User)

#Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

#Customers
class Customer(models.Model):
    first_name = models.CharField("First Name", max_length=20)
    last_name = models.CharField("Last Name", max_length=20)
    phone = models.CharField("Contact number", max_length=15)
    email = models.EmailField("Email Address")
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'

#Product details
class Product(models.Model):
    name = models.CharField("Product Name", max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, blank=True, null=True, default='')
    image = models.ImageField(upload_to='uplaods/product/')

    #add sale staff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name

#Customer Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField("Shipping Address", max_length=100, default='')
    phone = models.CharField("Contact number", max_length=15)
    date = models.DateTimeField(default=dt.datetime.now())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
