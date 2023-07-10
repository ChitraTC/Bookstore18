from django.contrib.auth.models import User
from django.db import models




# Create your models here.

STATE_CHOICES = (
    ('Delhi','Delhi'),
    ('Pune','Pune'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Tamilnadu','Tamilnadu')
)

CATEGORY_CHOICES=(
    ('KD','Kids'),
    ('TB','Textbook'),
    ('FT','Fiction'),
    ('TL','Thriller'),
    ('RM','Romance'),

)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=50)
    image_url = models.CharField(max_length=2083, blank=True)
    book_available = models.BooleanField()
    def __str__(self):
        return self.title



class Order(models.Model):
    product = models.ForeignKey(Book, max_length=200, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=200)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.book.price





# class CartItem(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#
#     def __str__(self):
#         return f'{self.quantity} * {self.book}'
#
#     @property
#     def total_price(self):
#         return self.book.price * self.quantity

