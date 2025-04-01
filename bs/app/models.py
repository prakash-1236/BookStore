from itertools import product
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


#Create your models here.
STATE_CHOICES = [
    ('AN', 'Andaman & Nicobar Islands'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CH', 'Chandigarh'),
    ('CG', 'Chhattisgarh'),
    ('DN', 'Dadra & Nagar Haveli'),
    ('DD', 'Daman and Diu'),
    ('DL', 'Delhi'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu & Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('LD', 'Lakshadweep'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PY', 'Puducherry'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UK', 'Uttarakhand'),
    ('UP', 'Uttar Pradesh'),
    ('WB', 'West Bengal'),
]

# Define category choices
CATEGORY_CHOICES = [
    ('NF', 'Non-Fiction'),
    ('F', 'Fiction'),
    ('LR', 'Love & Romance'),
    ('T', 'Thriller'),
    ('SF', 'Science Fiction'),
    ('AA', 'Action & Adventure'),
    ('D', 'Drama'),
    ('C', 'Comedy'),
    ('P', 'Poetry'),
    ('CL', 'Classic'),
    ('YA', 'Young Adult'),
]

class Product(models.Model):
    title = models.CharField(max_length=200)
    discounted_price = models.FloatField()
    selling_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='', blank=True)
    prodapp = models.TextField(default='', blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    product_image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title
    

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, unique=True) 
    zipcode = models.CharField(max_length=10)  
    state = models.CharField(choices=STATE_CHOICES, max_length=2)  

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ✅ Correct (lowercase p)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price  # ✅ Update this too


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - ₹{self.amount}"

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.product.title} ({self.quantity})"

    def save(self, *args, **kwargs):
        """
        Automatically update the order status based on payment.
        """
        if self.payment and self.payment.paid:
            self.status = "Accepted"
        super().save(*args, **kwargs)



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'product')  # Prevents duplicate wishlist entries

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
