from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class MedicineCategory(models.Model):
    """Categories for medicines"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Medicine Categories"
        ordering = ['name']


class Medicine(models.Model):
    """Medicine/Drug model"""
    
    PRESCRIPTION_CHOICES = (
        ('otc', 'Over The Counter'),
        ('prescription', 'Prescription Required'),
        ('controlled', 'Controlled Substance'),
    )
    
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE, related_name='medicines')
    
    # Medical Information
    active_ingredients = models.TextField()
    strength = models.CharField(max_length=100)  # e.g., "500mg", "10ml"
    dosage_form = models.CharField(max_length=50)  # e.g., "tablet", "syrup", "injection"
    
    # Usage Information
    indications = models.TextField(help_text="What conditions this medicine treats")
    dosage_instructions = models.TextField()
    side_effects = models.TextField(blank=True, null=True)
    contraindications = models.TextField(blank=True, null=True)
    warnings = models.TextField(blank=True, null=True)
    
    # Regulatory Information
    prescription_type = models.CharField(max_length=20, choices=PRESCRIPTION_CHOICES, default='otc')
    manufacturer = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    manufacturing_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    # Inventory Information
    stock_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Additional Information
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.strength})"
    
    @property
    def discounted_price(self):
        """Calculate price after discount"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
    
    @property
    def is_in_stock(self):
        """Check if medicine is in stock"""
        return self.stock_quantity > 0
    
    @property
    def is_expired(self):
        """Check if medicine is expired"""
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False
    
    class Meta:
        ordering = ['name', 'strength']


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"
    
    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.medicine.discounted_price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'medicine')


class Order(models.Model):
    """Customer orders"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    order_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Order Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping Information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_phone = models.CharField(max_length=15)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    # Special Instructions
    notes = models.TextField(blank=True, null=True)
    prescription_image = models.ImageField(upload_to='prescriptions/', blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)
    
    def generate_order_id(self):
        """Generate unique order ID"""
        import random
        import string
        return 'ORD' + ''.join(random.choices(string.digits, k=8))
    
    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Prescription(models.Model):
    """Prescription uploads for prescription medicines"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='prescriptions', blank=True, null=True)
    
    prescription_image = models.ImageField(upload_to='prescriptions/')
    doctor_name = models.CharField(max_length=200)
    doctor_license = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='verified_prescriptions')
    verification_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Prescription for {self.user.username} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    """Medicine reviews by users"""
    
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicine_reviews')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='reviews')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Effectiveness questions
    effectiveness = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    side_effects_experienced = models.BooleanField(default=False)
    would_recommend = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medicine.name} - {self.rating} stars by {self.user.username}"
    
    class Meta:
        unique_together = ('user', 'medicine', 'order_item')
        ordering = ['-created_at']