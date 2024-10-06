from django.db import models
from django.core.validators import MinValueValidator

class Vendor_Registration(models.Model):
    username = models.CharField(max_length=150, unique=True) 
    email = models.EmailField()  
    password = models.CharField(max_length=255)  
    confirm_password = models.CharField(max_length=255)  

    def __str__(self):
        return self.username
    
class Product(models.Model):
    vendor = models.ForeignKey(Vendor_Registration, on_delete=models.CASCADE, related_name='products')
  
    name = models.CharField(max_length=150)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True) 
    photo = models.FileField(upload_to='product_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class User_Registration(models.Model):
    username = models.CharField(max_length=150, unique=True) 
    email = models.EmailField()  
    password = models.CharField(max_length=255)  # Password field
    confirm_password = models.CharField(max_length=255)  # Confirm password field
    Address=models.TextField(blank=False)

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was added

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the order was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the order was last updated

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of order

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"